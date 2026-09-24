import discord
from discord.ext import commands
import os
from utils.app_command_handler import handle_app_command_error

class PracticeBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix=".",
            intents=discord.Intents.all()
        )

    async def setup_hook(self):

        self.tree.on_error = handle_app_command_error

        print("SETUP HOOK EXECUTADO")

        diretorio = "cogs"

        print("Diretorio atual:", os.getcwd())
        print("Cogs existe?", os.path.exists(diretorio))

        for root, dirs, files in os.walk(diretorio):

            print("ROOT:", root)
            print("FILES:", files)

            for file in files:

                if file.endswith(".py") and file != "__init__.py":

                    caminho_ajustado = (
                        os.path.join(root, file)
                        .replace("\\", ".")
                        .replace("/", ".")[:-3]
                    )

                    print("CARREGANDO:", caminho_ajustado)

                    try:
                        await self.load_extension(caminho_ajustado)

                        print("CARREGADO:", caminho_ajustado)

                    except Exception as e:

                        print("ERRO:", caminho_ajustado, repr(e))

        await self.tree.sync()