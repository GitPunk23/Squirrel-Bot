from discord.ext import commands
from datetime import datetime, timedelta
from data_manager import data_manager
from silly import buff_threat

next_poker_night = datetime.utcnow() + timedelta(days=7)
house_chips = 10000
poker_night_flag = False
poker_night_start_time = None
poker_night_end_time = None

def setup(bot):
    @bot.command(name='poker-start')
    async def start_poker_night(ctx):
        global poker_night_flag, poker_night_start_time

        # Check if poker night is already running
        if poker_night_flag:
            await ctx.send("Poker night is already in progress.")
            return

        # Start poker night
        poker_night_flag = True
        poker_night_start_time = datetime.utcnow()

        await ctx.send("Let the poker night begin!")

    @bot.command(name='poker-stop')
    async def stop_poker_night(ctx):
        global poker_night_flag, poker_night_start_time

        if not poker_night_flag:
            await ctx.send("Poker night is not in progress.")
            return
        
        poker_night_flag = False
        poker_night_end_time = datetime.utcnow()

        # Calculate the duration of the poker night
        duration = poker_night_end_time - poker_night_start_time

        await ctx.send(f"Poker night has ended. It lasted for {duration}.")    

    @bot.command(name='house')
    async def check_house_chips(ctx):
        global house_chips

        await ctx.send(f"The house currently has won {house_chips} chips.")

    @bot.command(name='poker-join')
    async def join_game(ctx):

        await buff_threat(ctx)


