import discord

from settings.bot import PracticeBot
from settings.config import Config

bot = PracticeBot()
bot.run(Config.TOKEN)