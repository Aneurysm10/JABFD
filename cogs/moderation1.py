import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta
import datetime
from repository.mod_repo import ModerationRepository
from database.connection import AsyncSessionLocal

class Mod(commands.GroupCog, group_name="moderation"):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()


    @app_commands.command(name='ban', description='Bans a member from the server')
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    @app_commands.describe(user='Input member id or mention member', reason='Provide reason')
    async def ban_user(self, interaction: discord.Interaction, user: discord.User, * ,reason: str | None):
        await interaction.response.defer()

        async with AsyncSessionLocal() as session:
            try:
                await interaction.guild.ban(user, reason=reason)

                case = await ModerationRepository.create_ban(
                    session,
                    guild_id=interaction.guild.id,
                    user_id=user.id,
                    moderator_id=interaction.user.id,
                    reason=reason
                )

                await session.commit()

            except (discord.HTTPException, discord.Forbidden, discord.NotFound):
                await session.rollback()
                raise

        await interaction.followup.send(f"{user.mention} was banned")

    @app_commands.command(name='kick', description='Kicks a member from the server')
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.bot_has_permissions(kick_members=True)
    @app_commands.describe(member='Provide member', reason='the reason for the kick')
    async def kick_user(self, interaction: discord.Interaction, member: discord.Member, * ,reason: str | None):

        await interaction.response.defer()


        async with AsyncSessionLocal() as session:
            try:

                await interaction.guild.kick(member, reason=reason)

                case = await ModerationRepository.create_kick(
                    session,
                    guild_id=interaction.guild.id,
                    user_id=member.id,
                    moderator_id=interaction.guild.id,
                    reason=reason
                )

                await session.commit()

            except (discord.HTTPException, discord.Forbidden, discord.NotFound):
                await session.rollback()
                raise


        await interaction.followup.send(f'**{member.mention}** was kicked')

    @app_commands.command(name='timeout', description='Mutes a member from the server')
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.checks.bot_has_permissions(moderate_members=True)
    @app_commands.describe(member='Provide member', reason='Provide reason')
    async def timeout_user(self, interaction: discord.Interaction, member: discord.Member, minutes: int, * ,reason: str | None):
        await interaction.response.defer()

        async with AsyncSessionLocal() as session:
            try:
                duration = datetime.timedelta(minutes=minutes)

                await member.timeout(duration, reason=reason)

                case = await ModerationRepository.create_timeout(
                    session,
                    guild_id=interaction.guild.id,
                    user_id=member.id,
                    moderator_id=interaction.user.id,
                    reason=reason
                )

                await session.commit()

            except (discord.HTTPException, discord.Forbidden, discord.NotFound):
                await session.rollback()
                raise

        await interaction.followup.send(f"{member.mention} was muted")

    @app_commands.command(name='unban', description='Unbans a member')
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    @app_commands.describe(user='Input member id')
    async def unban_user(self, interaction: discord.Interaction, user: discord.User):
        await interaction.response.defer()

        async with AsyncSessionLocal() as session:
            try:
                await interaction.guild.unban(user)

                case = await ModerationRepository.remove_ban(
                    guild_id=interaction.guild.id,
                    user=user.id
                )

                await session.commit()

            except (discord.HTTPException, discord.Forbidden, discord.NotFound):
                await session.rollback()
                raise


    @app_commands.command(name='removetimeout', description='Remove timeout from a member')
    @app_commands.describe(member='Provide member')
    async def unmute_user(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer()

        async with AsyncSessionLocal() as session:
            try:
                await member.timeout(None)

                case = await ModerationRepository.remove_the_timeout(
                    session,
                    guild_id=interaction.guild.id,
                    user_id=member.id
                )

                await session.commit()

            except (discord.HTTPException, discord.Forbidden, discord.NotFound):
                await session.rollback()
                raise


        await interaction.followup.send(f'**{member.mention}** was unmuted')

    @app_commands.command(name='purge', description='Clears a certain number of messages from the channel')
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    @app_commands.describe(amount='input number of messages')
    async def purge_command(self, interaction: discord.Interaction, amount: int):

        await interaction.response.defer()

        await interaction.channel.purge(limit=amount)

    @app_commands.command(name='warn', description='Warns a member')
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.checks.bot_has_permissions(moderate_members=True)
    @app_commands.describe(member="Provide member", reason="Provide reason")
    async def warn_member(self, interaction: discord.Interaction, member: discord.Member, * ,reason: str | None):

        await interaction.response.defer()

        async with AsyncSessionLocal() as session:

            case = await ModerationRepository.create_warn(
                session,
                guild_id=interaction.guild.id,
                user_id=member.id,
                moderator_id=interaction.user.id,
                reason=reason
            )

            await session.commit()

            get_warn = await ModerationRepository.get_user_warns(
                session,
                guild_id=interaction.guild.id,
                user_id=member.id
            )

            user_warns = len(get_warn)

            if user_warns == 3:
                try:
                    await interaction.guild.ban(member, reason=reason)
                    case_ban = await ModerationRepository.create_ban(
                        session,
                        guild_id=interaction.guild.id,
                        user_id=member.id,
                        moderator_id=interaction.user.id,
                        reason=reason
                    )

                    await session.commit()

                except (discord.HTTPException, discord.Forbidden, discord.NotFound):
                    await session.rollback()
                    raise


            await interaction.followup.send(f"{member.mention} has been warned")

    @app_commands.command(name="unwarn", description="Removes a warning from a user")
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.checks.bot_has_permissions(moderate_members=True)
    @app_commands.describe(user='Input member id or mention member')
    async def remove_the_warn(self, interaction: discord.Interaction, user: discord.User):
        await interaction.response.defer()

        async with AsyncSessionLocal() as session:

            case = await ModerationRepository.remove_warn(
                session,
                guild_id=interaction.guild_id,
                user_id=user.id,
            )

            await session.commit()

        await interaction.followup.send(f"{user.mention} was unwarned")

    @app_commands.command(name="warnlist", description="Send a list of user warnings")
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.checks.bot_has_permissions(moderate_members=True)
    @app_commands.describe(user="Provide user")
    async def send_warnlist(self, interaction: discord.Interaction, user: discord.User):
        await interaction.response.defer()

        async with AsyncSessionLocal() as session:
            warns = await ModerationRepository.get_user_warns(
                session,
                guild_id=interaction.guild.id,
                user_id=user.id
            )

            embed = discord.Embed(
                title=f"warnlist from {user.name}",
                color=discord.Color.dark_red()
            )

            embed.set_thumbnail(url=user.avatar)

            for case in warns:
                embed.add_field(name=f"**Case ID:** {case.id}", value=f"**Reason:** {case.reason}\n **Moderator ID:** {case.moderator_id}", inline=False)

            await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Mod(bot))
