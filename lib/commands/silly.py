import discord
from discord.ext import commands

# VARIABLES
SMACKFLAG = True

# FUNCTIONS
async def buff_threat(ctx):
    threatMessage = f"{ctx.author.mention} Hey bud, how you like those kneecaps?"
    with open('resources/img/bot/squirrel.webp', 'rb') as image:
        threatImage = discord.File(image)
    await ctx.send(content=threatMessage, file=threatImage)
    return 

# ATTACH TO BOT
async def setup(bot):
    
    # ON MESSAGE EVENTS
    #@bot.event
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
    
    # COMMANDS


    