import os
import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import importlib.util
import json
import re
import asyncio

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
            "total_scores": {},
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
            
        if result == 'X':
            score_value = 0
        else:
            score_value = 1

        if game not in data["players"][player_id]["total_scores"]:
            data["players"][player_id]["total_scores"][game] = 0
        data["players"][player_id]["total_scores"][game] += score_value

        if game not in data["players"][player_id]["today_scores"]:
            data["players"][player_id]["today_scores"][game] = 0
        data["players"][player_id]["today_scores"][game] = result

        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
            
        return True
    
    async def display_scoreboard(self, ctx):
        json_file = 'data/puzzle_games/player_data.json'
        with open(json_file, 'r') as f:
            data = json.load(f)

        game_order = ["wordle", "connections", "costcodle", "spotle", "bandle", "pokedoku"]

        header_row = ["Player"] + [game.capitalize() for game in game_order]

        table_rows = [header_row]
        for player_id, player_data in data["players"].items():
            user = await self.bot.fetch_user(int(player_id))
            if user:
                player_name = user.display_name
            else:
                player_name = f"Unknown User (ID: {player_id})"
            row = [f"{player_name}"] 
            for game in game_order:
                score = player_data["today_scores"].get(game, "-")
                row.append("-" if score == 0 else score)
            table_rows.append(row)

        embed = discord.Embed(title="Today's Scores", color=discord.Color.blue())
        for row in table_rows:
            row_values_str = " | ".join(str(cell) for cell in row)
            embed.add_field(name=row[0], value=row_values_str, inline=False)

        await ctx.send(embed=embed)

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
        await self.display_scoreboard(ctx)
        
    @tasks.loop(hours=24)
    async def reset_daily_scores(self):
        with open('data/puzzle_games/player_data.json', 'r') as f:
            data = json.load(f)

        for player_id, player_data in data["players"].items():
            player_data["today_scores"] = {game: 0 for game in player_data["today_scores"]}

        with open('data/puzzle_games/player_data.json', 'w') as f:
            json.dump(data, f, indent=4)
        
    @commands.Cog.listener()
    async def on_ready(self):
        now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        est = pytz.timezone('US/Eastern')
        now_est = now_utc.astimezone(est)
        midnight_est = (now_est + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        delta = midnight_est - now_est

        print(f"Sleeping for {delta} seconds before beginning reset score task")
        await asyncio.sleep(delta.total_seconds())
        await self.reset_daily_scores()
        
        
async def setup(bot):
    await bot.add_cog(PuzzleGames(bot))
