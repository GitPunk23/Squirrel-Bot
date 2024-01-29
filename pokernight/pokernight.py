# In pokernight/pokernight.py
from discord.ext import commands

def setup(bot):
    @bot.command(name='start_poker_night')
    async def start_poker_night(ctx):
        await ctx.send("Let the poker night begin!")

    @bot.command(name='say_hi')
    async def say_hi(ctx):
        # Check if the user who invoked the command said "hi"
        if "hi" in ctx.message.content.lower():
            await ctx.send("hi")

    @bot.command(name='test')
    async def test_command(ctx):
        await ctx.send("Testing command!")

