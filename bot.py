import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands
from lib.poker_night.poker_night import PokerNight
from lib.commands.silly import Silly
from lib.data_manager import data_manager
from lib.poke_battle.poke import Poke
from lib.puzzle_games.puzzle_games import PuzzleGames

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
intents.members = True
intents.messages = True  
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await setup(bot)


async def setup(client):
    await bot.add_cog(PokerNight(bot))
    await bot.add_cog(Silly(bot))
    await bot.add_cog(Poke(bot))
    await bot.add_cog(PuzzleGames(bot))


bot.run(TOKEN)
