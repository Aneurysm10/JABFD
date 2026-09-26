import discord
from discord import app_commands
from discord.ext import commands
import time
import psutil

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name='ping', description='Sends pong')
    async def ping_command(self, interaction: discord.Interaction):

        bot_latency = round(self.bot.latency * 1000)

        await interaction.response.send_message(f'Pong!\n **Guild:** {interaction.guild.id}\n **Bot latency:** {bot_latency}ms\n **Discord.py:** 2.7.1')

    @app_commands.command(name='avatar', description='Gives you a members avatar')
    @app_commands.describe(user='Provide user')
    async def show_avatar(self, interaction: discord.Interaction, user: discord.User):

        target = user or interaction.user

        avatar_url = target.display_avatar

        embed = discord.Embed(
            title=f'Avatar for {target}',
            color=discord.Color.dark_gray()
        )

        if target.avatar:
            embed.set_image(url=avatar_url)

        else:
            embed.set_image(url=target.default_avatar.url)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='userinfo', description='Shows your discord account information or information from another user')
    @app_commands.describe(member='Provide member')
    async def userinfo_command(self, interaction: discord.Interaction, member: discord.Member):

        member = member or interaction.user

        embed = discord.Embed(
            title=f'User Info for {member}',
            color=discord.Color.dark_blue()
        )

        embed.set_thumbnail(url=member.display_avatar)
        embed.add_field(name=f'Name', value=f'{member.display_name}')
        
        embed.add_field(name=f'Discord Joined date', value=f'{member.created_at.strftime("%d/%m/%Y")}', inline=False)
        embed.add_field(name=f'Server joined date', value=f'{member.joined_at.strftime("%d/%m/%Y")}', inline=False)


        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='serverinfo', description='Shows server information')
    async def serverinfo_command(self, interaction: discord.Interaction):

        created_at = interaction.guild.created_at.strftime("%b %d %Y")

        embed = discord.Embed(
            title=f'{interaction.guild.name} Information',
            color=discord.Color.blue()
        )

        embed.add_field(name='Server ID', value=f'{interaction.guild.id}', inline=False)
        embed.add_field(name='Created On', value=f'{created_at}', inline=False)
        embed.add_field(name='Owner', value=f'{interaction.guild.owner}', inline=False)
        embed.add_field(name='Members', value=f'{interaction.guild.member_count}', inline=False)
        embed.add_field(name='Channels', value=len(interaction.guild.text_channels))

        if interaction.guild.icon:
            embed.set_thumbnail(url=interaction.guild.icon.url)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="about", description="Shows some stats about the bot")
    async def uptime_command(self, interaction: discord.Interaction):
        timeUp = time.monotonic() - self.bot.startTime
        hours = int(timeUp / 3600)
        minutes = int((timeUp / 60) // 60)
        seconds = int(timeUp % 60)

        embed = discord.Embed(
            title="**Some info about the bot**",
            color=discord.Color.dark_gray()
        )

        embed.add_field(name="Uptime", value=f"`{hours}h {minutes}m {seconds}s`", inline=True)
        embed.add_field(name="CPU Usage", value=f"`{psutil.cpu_percent()}%`", inline=True)
        embed.add_field(name="Memory Usage", value=f"`{psutil.virtual_memory().percent}%`", inline=True)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(GeneralCommands(bot))
