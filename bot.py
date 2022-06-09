import os

import discord
import random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
#print(os.getenv('DISCORD_TOKEN'))
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
bot = commands.Bot(command_prefix=';')

SMACKFLAG = True


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

@bot.command(
    brief='Prints an entry in the coordinates channel. Use: [Structure] [X coord] [Y coord] [Z coord] ["notes"]',
    help='A command that will print out a list of coordinates in another channel for display.'
)
@commands.has_role('Crafter')
async def coord(ctx, struc, x, y, z, notes=''): 
    coordsCH = bot.get_channel(984518790681362492)

    if x.isdigit() == False and y.isdigit() == False and z.isdigit() == False:
        await ctx.send('Incorrect format\nExample: ;coord Mineshaft 50 15 -789 "A big mineshaft"\n(Description/Notes are optional)')
        return

    printString = ctx.message.author.mention + ' found a ' + struc + ' at:\nX: ' + x + '\nY: ' + y + '\nZ: ' + z
    if (notes != ''):
        printString += '\nThey said: ' + notes
    await coordsCH.send(printString)  
 

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