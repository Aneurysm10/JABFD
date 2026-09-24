import discord
from discord.ext import commands
import time

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name} has been loaded")
        self.bot.startTime = time.monotonic()
        await self.bot.change_presence(activity=discord.Game(name='Haunting Ducks'))

    @commands.Cog.listener()
    async def on_connect(self):
        print(f"{self.bot.user.name} has connected to Discord!")

    @commands.Cog.listener()
    async def on_disconnect(self):
        print(f"{self.bot.user.name} has disconnected from Discord!")

async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))