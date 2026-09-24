import discord
from discord.ext import commands
from discord import app_commands
import random

class FunCommands(commands.GroupCog, group_name="fun"):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name='reverse', description='sends a text reversed')
    @app_commands.describe(text='the text to reverse')
    async def reverse_text(self, interaction: discord.Interaction, text: str):

        reverse = text[::-1]
            
        await interaction.response.send_message(reverse)
    
    @app_commands.command(name='eightball', description='asks the magic 8ball')
    @app_commands.describe(question='make a question')
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
    
    
    @app_commands.command(name='coinflip', description='flips a coin')
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


    @app_commands.command(name='pick', description='chooses a random item from a sentence')
    @app_commands.describe(sentence="input sentence")
    async def pick_command(self, interaction: discord.Interaction, sentence: str):

        pick_list = sentence.replace(",", " ").split()
        pick_random = random.choice(pick_list)

        await interaction.response.send_message(f"{pick_random}")  

async def setup(bot: commands.Bot):
    await bot.add_cog(FunCommands(bot))