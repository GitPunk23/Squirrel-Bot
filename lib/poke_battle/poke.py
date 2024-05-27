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
        pokemon_P1 = Pokemon(self.generate_random_number())
        #retrieve pokemon 2
        pokemon_P2 = Pokemon(self.generate_random_number())
        #create and run battle
        

        message = f'{ctx.author.mention} \'s {pokemon_P1.species.capitalize()} battling against {pokemon_P2.species.capitalize()}!'

        await ctx.send(message)
        await self.test_embed(ctx, pokemon_P2)
        await self.test_embed(ctx, pokemon_P1)


    async def test_embed(self, ctx, pokemon):
        
        type_string = f"{pokemon.type_one}"
        if pokemon.type_two:
            type_string += f", {pokemon.type_two}"
            
        moves_list = "\n".join([f"• {move['name']}" for move in pokemon.moves])
        stats_list = "\n".join([f"• {stat}: {value}" for stat, value in pokemon.stats.items()])
            
        embed = self.create_embed(
            title=f"{pokemon.species.capitalize()} Lvl {pokemon.level}",
            description= f"""
            type: {type_string}
            health: {pokemon.current_hp}
            status: {pokemon.status_condition}
            """,
            color=0x73ff00,
            fields=[
                ("Attacks", moves_list, True),
                ("Stats", stats_list, True)
            ]
        )
        
        embed.set_thumbnail(url=pokemon.spriteURL)
        
        await ctx.send(embed=embed)


    def create_embed(self, title, description, color=discord.Color.blue(), fields=None, footer=None, author=None, thumbnail=None, image=None):
        embed = discord.Embed(title=title, description=description, color=color)
        
        if fields:
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
        
        if footer:
            embed.set_footer(text=footer)
        
        if author:
            embed.set_author(name=author['name'], icon_url=author['icon_url'], url=author.get('url'))
        
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        
        if image:
            embed.set_image(url=image)
        
        return embed
            

async def setup(bot):
    bot.add_cog(Poke(bot))
