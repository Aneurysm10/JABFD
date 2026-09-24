import logging
import discord

logger = logging.getLogger(__name__)

async def handle_generic_error(
        interaction: discord.Interaction,
        error: Exception
):
    if isinstance(error, discord.Forbidden):
        message = ("I do not have permission to peform this action!")

    elif isinstance(error, discord.NotFound):
        message = ("The request discord resource could not be found!")

    elif isinstance(error, discord.HTTPException):
        message = ("Discord returned an error while processing this request!")

    elif isinstance(error, discord.DiscordException):
        message = ("a discord-related error occurred  while processing this request!")

    else:
        logger.exception("Unhandled generic error!", exc_info=error)
        message = ("An unexpected error occurred!")

    try:
        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)

        else:
            await interaction.response.send_message(message, ephemeral=True)

    except discord.HTTPException:
        logger.exception("Failed to send generic error response!")