import os

import discord
import random
from dotenv import load_dotenv

load_dotenv()
#print(os.getenv('DISCORD_TOKEN'))
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is searching for nuts in:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #Array of words for the smack response
    butts = ["butt", "ass", "bend over", "caboose", "tushy", "rump", "booty", "peach",
             "bends over", "keister", "heiny", "heinie", "posterior", "behind"]
    messageContent = message.content.lower()

    #User requested response when "butt" or a similar word is sent 
    if any(butt in messageContent for butt in butts):
        response = '***smack*** ' #+ message.author.id 
        await message.channel.send(response)
        await message.add_reaction("🖐️")
    

client.run(TOKEN)
