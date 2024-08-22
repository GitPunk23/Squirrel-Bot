import os
import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from collections import defaultdict
import importlib.util
import pytz
import json
import re
import asyncio
import logging

logger = logging.getLogger(__name__)
NOT_PLAYED = '-'
LOST = 'X'
game_order = ["wordle", "connections", "costcodle", "spotle", "bandle", "pokedoku"]
channel_id = 775062415381364767

class PuzzleGames(commands.Cog):
    def __init__(self, bot):
        self.initialize_player_data()
        self.bot = bot
        self.wordle_regex = re.compile(r'Wordle \d{1,3}(?:,\d{3})* ((?:\d+|X))/6.*')
        self.connections_regex = re.compile(r'Connections\s+Puzzle\s+#(\d+)\n+(?:[⬛🟨🟦🟩🟪\n]+)')
        self.costcodle_regex = re.compile(r'Costcodle #\d+ ((?:\d+|X))/6.*')
        self.spotle_regex = re.compile(r'Spotle #(\d+)🎧\n\n[⬜🟩🟨🟥🟦🟪🟫🟧\n]+')
        self.bandle_regex = re.compile(r'Bandle #\d+ ((?:\d+|x))/\d+\n[⬛🟩🟨🟥⬜]+\nFound: \d+/\d+ \(\d+%\)')  
        self.pokedoku_regex = re.compile(
            r'(?::red_circle:|🌟) PokeDoku (?:Summary|Champion) (?:⚪️|🌟)\n'
            r'(?:By: .+|📅 \d{4}-\d{2}-\d{2})\n\n'
            r'Score: (\d+)/\d+\n'
            r'Uniqueness: (\d+)/\d+\n\n'
            r'([⬜⬛🟨🟩🟦🟪🟥✅\n ]+)\n\n'
            r'Play at: https://pokedoku.com')
        self.schedule_daily_reset()
        
    def schedule_daily_reset(self):
        self.bot.loop.create_task(self._wait_until_midnight_and_start_reset())
    
    def compare_score(self, player1_score, player2_score):
        draw = (isinstance(player1_score, int) and isinstance(player2_score, int)) and player1_score == player2_score
        if draw:
            return
        win_vs_win = (isinstance(player1_score, int) and isinstance(player2_score, int)) and player1_score > player2_score
        win_vs_loss = (isinstance(player1_score, int) and player2_score in ('X', '-'))
        loss_vs_unplayed = player1_score == 'X' and player2_score == '-'
        unplayed_vs_unplayed = player1_score == '-' and player2_score == '-'
        return win_vs_win or win_vs_loss or loss_vs_unplayed or unplayed_vs_unplayed
    
    def compare_players(self, player1_scores, player2_scores):
        if self.get_wins(player1_scores) > self.get_wins(player2_scores):
            return true
        
        if self.get_wins(player1_scores) == self.get_wins(player2_scores):
            player1 = 0
            player2 = 0
            for game in game_order:
                player1_score = player1_scores.get(game, 0)
                player2_score = player2_scores.get(game, 0)
                result = self.compare_score(player1_score, player2_score)
                if result is None:
                    continue
                elif result:
                    player1 += 1
                else: 
                    player2 += 1
                    
            return player1 > player2 or player1 == player2
            
    def get_wins(self, player_scores):
        player_score = 0
        for game in game_order:
            game_score = player_scores.get(game, 0)
            if isinstance(game_score, int):
                player_score += 1
                
        return player_score
    
    def wipe_scores(self):
        logger.info("Beginning player score reset...")
        with open('data/puzzle_games/player_data.json', 'r') as f:
            data = json.load(f)

        for player_id, player_data in data["players"].items():
            player_data["today_scores"] = {game: 0 for game in player_data["today_scores"]}

        with open('data/puzzle_games/player_data.json', 'w') as f:
            json.dump(data, f, indent=4)
            
        logger.info("Players scores have been reset!")

    async def _wait_until_midnight_and_start_reset(self):
        await self.bot.wait_until_ready()

        now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        est = pytz.timezone('US/Eastern')
        now_est = now_utc.astimezone(est)
        midnight_est = (now_est + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        delta = (midnight_est - now_est).total_seconds()

        logger.info(f"Sleeping for {delta} seconds before starting the daily reset task")
        await asyncio.sleep(delta)

        # Start the reset task loop
        self.reset_daily_scores_task.start()
  
    async def parse_connections_score(self, message):
        player_id = str(message.author.id)
        content = message.content

        lines = content.split('\n')
        rows = lines[2:]

        correct_rows = 0
        tries = len(rows)
        for row in rows:
            if len(set(row.strip())) == 1:
                correct_rows += 1

        if correct_rows == 4:
            return int(tries)
        else:
            return 'X'        
    
    async def parse_spotle_score(self, message):
        content = message.content
        match = self.spotle_regex.match(content)
        game_board = match.group(0)  # The entire matched string

        tries = game_board.count('⬜') + 1
        
        if '🟩' in game_board:
            return int(tries)
        else: 
            return 'X'
                           
    async def add_player(self, player_id, json_file):
        if not os.path.exists(json_file):
            data = {"players": {}}
        else:
            with open(json_file, 'r') as f:
                data = json.load(f)
        
        if player_id in data["players"]:
            print("Player already exists.")
            return False
    
        data["players"][player_id] = {
            "today_scores": {}
        }
        
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        return True
      
    async def check_for_regex(self, message):
        if self.wordle_regex.match(message.content):
            match = self.wordle_regex.match(message.content)
            game = "wordle"
            result = match.group(1)
            
        elif self.connections_regex.match(message.content):
            game = "connections"
            result = await self.parse_connections_score(message)
        
        elif self.costcodle_regex.match(message.content):
            match = self.costcodle_regex.match(message.content)
            game = "costcodle"
            result = match.group(1)
        
        elif self.spotle_regex.match(message.content):
            game = "spotle"
            result = await self.parse_spotle_score(message)
        
        elif self.bandle_regex.match(message.content):
            match = self.bandle_regex.match(message.content)
            game = "bandle"
            result = match.group(1).upper()
        
        elif self.pokedoku_regex.match(message.content):
            match = self.pokedoku_regex.match(message.content)
            game = "pokedoku"
            
            if int(match.group(1)) == 9:
                result = int(match.group(2))
            else:
                result = 'X'
            
        else:
            game = False
            result = False
         
        return game, result
    
    async def sort_players(self, data):
        players_list = list(data.items())
        scores_type = "today_scores"

        n = len(players_list)
        for i in range(n - 1):
            for j in range(n - 1 - i):
                player1_id, player1_data = players_list[j]
                player2_id, player2_data = players_list[j + 1]
                if not self.compare_players(player1_data[scores_type], player2_data[scores_type]):  
                    players_list[j], players_list[j + 1] = players_list[j + 1], players_list[j]
        
        return dict(players_list)
    
    async def update_player_score(self, player_id, game, result):
        json_file = 'data/puzzle_games/player_data.json'
        
        if not os.path.exists(json_file):
            os.makedirs(os.path.dirname(json_file), exist_ok=True)
            with open(json_file, 'w') as f:
                json.dump(initial_structure, f)
        
        with open(json_file, 'r') as f:
            data = json.load(f)

        if player_id not in data["players"]:
            await self.add_player(player_id, json_file)
            
        if game in data["players"][player_id]["today_scores"] and data["players"][player_id]["today_scores"][game] != 0:
            return False

        if game not in data["players"][player_id]["today_scores"]:
            data["players"][player_id]["today_scores"][game] = 0
        data["players"][player_id]["today_scores"][game] = result

        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
            
        return True
    
    async def get_scoreboard(self):
        json_file = 'data/puzzle_games/player_data.json'
        with open(json_file, 'r') as f:
            data = json.load(f)

        header_row = [game.capitalize() for game in game_order]

        sorted_players = await self.sort_players(data["players"])

        embed = discord.Embed(title="Today's Scores", color=discord.Color.blue())
        header_str = f"| {' | '.join(header_row)} |"
        embed.add_field(name="Games", value=header_str, inline=False)

        position = 1
        for player_id in sorted_players:
            try:
                user = await self.bot.fetch_user(int(player_id))
                player_name = user.name
            except discord.errors.NotFound:
                player_name = f"Unknown User (ID: {player_id})"
            row = [player_name]
            for game in game_order:
                score = data["players"][player_id]["today_scores"].get(game, float('inf'))
                row.append("-" if score == float('inf') or score == 0 else score)
            row_values_str = f"| {' | '.join(str(cell) for cell in row[1:])} |"
            
            position_and_name = f"{position} - {player_name}"
            embed.add_field(name=position_and_name, value=row_values_str, inline=False)
            position+=1

        return embed

    def initialize_player_data(self):
        json_file = 'data/puzzle_games/player_data.json'
        if not os.path.exists(json_file):
            os.makedirs(os.path.dirname(json_file), exist_ok=True)
            with open(json_file, 'w') as f:
                initial_structure = {"players": {}}
                json.dump(initial_structure, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        game, result = await self.check_for_regex(message) 
        if not game:
            return
        else:
            await message.delete()
        
        player_id = message.author.id
        updated = await self.update_player_score(str(player_id), game, result)
        
        if not updated:
            await message.channel.send(f"{message.author.mention} already submitted a {game} score today...")
            return
        
        if game == "pokedoku":
            score_string = f"with a uniqueness of {result}!"
        else:
            score_string = f"in {result} tries!"
        
        if result == 'X':
              await message.channel.send(f"{message.author.mention} lost {game}!")
        else:
              await message.channel.send(f"{message.author.mention} won {game} {score_string}")
            
    @commands.command(name='join_puzzles')
    async def join_puzzles(self, ctx):
        await ctx.message.delete()
        player_id = str(ctx.author.id)
        json_file = 'data/puzzle_games/player_data.json'
        player_added = await self.add_player(player_id, json_file)
        if (player_added):
            await ctx.send(f"{ctx.author.mention} has joined puzzle games!")
        else:
            await ctx.send(f"{ctx.author.mention} is already registered for puzzles")

    @commands.command(name='scoreboard')
    async def scoreboard(self, ctx):
        await ctx.message.delete()
        await ctx.send(embed=await self.get_scoreboard())
        
    @commands.command(name='wipe')
    @commands.has_permissions(administrator=True)
    async def force_wipe(self, ctx):
        await ctx.message.delete()
        self.wipe_scores()
        
    @tasks.loop(hours=24)
    async def reset_daily_scores_task(self):
        logger.info("Displaying Scoreboard")
        channel_name = 'bot spam'
        channel = self.bot.get_channel(channel_id)
        await channel.send(embed=await self.get_scoreboard())
        self.wipe_scores()
        
