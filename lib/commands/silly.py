import discord
from discord.ext import commands

class Silly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Variables
    SMACKFLAG = True

    # Functions
    async def buff_threat(self, ctx):
        threatMessage = f"{ctx.author.mention} Hey bud, how you like those kneecaps?"
        with open('resources/img/bot/squirrel.webp', 'rb') as image:
            threatImage = discord.File(image)
        await ctx.send(content=threatMessage, file=threatImage)
        return 

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # Read message content as lowercase    
        messageContent = message.content.lower()

        # Array of words for the smack response
        butts = ["butt", "ass", "bend over", "caboose", "tushy", "rump", "booty", "peach",
                "bends over", "keister", "heiny", "heinie", "posterior", "behind", "dumpy", 
                "dump truck",]
        
        # User requested response when "butt" or a similar word is sent 
        if any(butt in messageContent for butt in butts) and self.SMACKFLAG:
            response = '***smack***'
            await message.channel.send(response)
            await message.add_reaction("🖐️")

    # Commands
    @commands.command()
    async def buff(self, ctx):
        await self.buff_threat(ctx)
