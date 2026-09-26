import discord
from discord.ext import commands
from discord import app_commands
import random

class FunCommands(commands.GroupCog, group_name="fun"):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name='reverse', description='Sends a reversed text')
    @app_commands.describe(sentence='Input sentence')
    async def reverse_text(self, interaction: discord.Interaction, sentence: str):

        reverse = sentence[::-1]
            
        await interaction.response.send_message(reverse)
    
    @app_commands.command(name='eightball', description='Asks the magic 8ball')
    @app_commands.describe(question='Input question')
    async def ask(self, interaction: discord.Interaction, question: str):

        possibilities = [
                    'no',
                    'It is certain.',
                    'It is decidedly so.',
                    'Without a doubt.',
                    'Yes - definitely.',
                    'You may rely on it.',
                    'Most likely.',
                    'Outlook good.',
                    'Yes.',
                    ]
            
        responses = random.choice(possibilities)
            
        embed = discord.Embed(
            title=f"{interaction.user.display_name}",
            description=f"{responses}",
            color=discord.Color.random()
        )
            
        await interaction.response.send_message(embed=embed)
    
    
    @app_commands.command(name='coinflip', description='Flips a coin')
    async def flip_coin(self, interaction: discord.Interaction):

        coin = ['Heads', 'Tails']
            
        flip = random.choice(coin)
            
        embed = discord.Embed(
            title=f"{interaction.user.display_name} flipped a coin",
            description=f"🪙{flip}",
            color=discord.Color.random()
        )
    
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="clapify", description="👋makes👋a👋text👋look👋like👋this👋")
    @app_commands.describe(sentence="input sentence")
    async def clapify_command(self, interaction: discord.Interaction, sentence: str):
        clapify_text = "👋" + "👋".join(sentence.split()) + "👋"

        await interaction.response.send_message(f"{clapify_text}")

    @app_commands.command(name='pick', description='Chooses a random element from the supplied choices')
    @app_commands.describe(sentence="Input sentence")
    async def pick_command(self, interaction: discord.Interaction, sentence: str):

        pick_list = sentence.replace(",", " ").split()
        pick_random = random.choice(pick_list)

        await interaction.response.send_message(f"{pick_random}")  

async def setup(bot: commands.Bot):
    await bot.add_cog(FunCommands(bot))
