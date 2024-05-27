import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands
from lib.poker_night import poker_night
from lib.commands import silly
from lib.data_manager import data_manager
from lib.poke_battle import poke
from lib.puzzle_games import puzzle_games

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
# --------------------------------------------------------------------------------------------------
# LOAD COMMANDS
poker_night.setup(bot)
silly.setup(bot)
poke.setup(bot)
puzzle_games.setup(bot)


bot.run(TOKEN)
