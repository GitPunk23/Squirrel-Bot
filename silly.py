import discord
from discord.ext import commands

async def buff_threat(ctx):
    threatMessage = f"{ctx.author.mention} Hey bud, how you like those kneecaps?"
    with open('Resources/bot_images/squirrel.webp', 'rb') as image:
        threatImage = discord.File(image)
    await ctx.send(content=threatMessage, file=threatImage)
    return 


    