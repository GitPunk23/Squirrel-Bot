import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands
from pokernight import pokernight

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
intents.members = True
intents.messages = True  # Add this line to enable message content intent
bot = commands.Bot(command_prefix=':', intents=intents)

pokernight.setup(bot)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is searching for nuts in:\n'
        f'{guild.name}(id: {guild.id})'
    )

# ------------------------------------------------------------------------------------

#VARIABLES
SMACKFLAG = True

#ON MESSAGE EVENTS
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return

    #Read message content as lowercase    
    messageContent = message.content.lower()

    #Array of words for the smack response
    butts = ["butt", "ass", "bend over", "caboose", "tushy", "rump", "booty", "peach",
             "bends over", "keister", "heiny", "heinie", "posterior", "behind", "dumpy", 
             "dump truck",]
    
    #User requested response when "butt" or a similar word is sent 
    if any(butt in messageContent for butt in butts) & SMACKFLAG == True:
        response = '***smack***'
        await message.channel.send(response)
        await message.add_reaction("🖐️")

    

bot.run(TOKEN)
