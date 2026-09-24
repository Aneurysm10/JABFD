import logging
import discord
from utils.generic_handler import handle_generic_error

from discord import app_commands

logger = logging.getLogger(__name__)

async def handle_app_command_error(
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
):

    if isinstance(error, app_commands.MissingPermissions):
        message = ("You do not have the required permissions to use this command1")

    elif isinstance(error, app_commands.BotMissingPermissions):
        message = ("I do not have the required permissions to execute this command!")

    elif isinstance(error, app_commands.TransformerError):
         message = ("One or more of the provided arguments are invalid")

    elif isinstance(error, app_commands.NoPrivateMessage):
            message = ("This command can only be used inside a server")

    elif isinstance(error, app_commands.CheckFailure):
        message = str(error) or "You cannot use this comamnd"

    elif isinstance(error, app_commands.CommandInvokeError):
         await handle_generic_error(interaction, error.original)
         return
         
    else:
         await handle_generic_error(interaction, error)
         return
         

    try:
         if interaction.response.is_done():
              await interaction.followup.send(message, ephemeral=True)

         else:
             await interaction.response.send_message(message, ephemeral=True)

    except discord.HTTPException:
        logger.exception("Failed to send application command error response!")