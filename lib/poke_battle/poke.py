import discord
import random
from discord.ext import commands
from lib.poke_battle.pokemon import Pokemon

class Poke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def generate_random_number(self):
        return random.randint(1, 1025)

    @commands.command(name='battle')
    async def battle(self, ctx):
 
        #retrieve pokemon 1
        pokemon_one = Pokemon(self.generate_random_number())
        #retrieve pokemon 2
        pokemon_two = Pokemon(self.generate_random_number())
        #create and run battle
        

        message = f'{pokemon_one.species} battling against {pokemon_two.species}!\n{pokemon_one.spriteURL}\n{pokemon_two.spriteURL}'
        await ctx.send(message)


        
    

def setup(bot):
    bot.add_cog(Poke(bot))
