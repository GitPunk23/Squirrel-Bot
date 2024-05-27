from discord.ext import commands
from datetime import datetime, timedelta
from lib.commands import silly

# Define global variables
next_poker_night = datetime.utcnow() + timedelta(days=7)
house_chips = 10000
poker_night_flag = False
poker_night_start_time = None
poker_night_end_time = None

# Define commands and events
class PokerNight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='poker')
    async def poker_help(self, ctx):
        await ctx.send("Here are the commands for poker:")
    
    @commands.command(name='poker-start')
    async def start_poker_night(self, ctx):
        global poker_night_flag, poker_night_start_time

        if poker_night_flag:
            await ctx.send("Poker night is already in progress.")
            return

        poker_night_flag = True
        poker_night_start_time = datetime.utcnow()

        await ctx.send("Let the poker night begin!")

    @commands.command(name='poker-stop')
    async def stop_poker_night(self, ctx):
        global poker_night_flag, poker_night_start_time, poker_night_end_time

        if not poker_night_flag:
            await ctx.send("Poker night is not in progress.")
            return
        
        poker_night_flag = False
        poker_night_end_time = datetime.utcnow()
        duration = poker_night_end_time - poker_night_start_time

        await ctx.send(f"Poker night has ended. It lasted for {duration}.")    

    @commands.command(name='poker-house')
    async def check_house_chips(self, ctx):
        global house_chips
        await ctx.send(f"The house currently has won {house_chips} chips.")

    @commands.command(name='poker-join')
    async def join_game(self, ctx):
        await silly.buff_threat(ctx)
        #await ctx.send("Placeholder for join_game command.")

async def setup(bot):
    bot.add_cog(PokerNight(bot))
