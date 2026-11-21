import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_ID = os.getenv("SERVER_ID")

class LauncherBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix="$",
            intents=intents
        )
        
    async def setup_hook(self):
        await self.load_extension("cogs.rbxrequests")
        print("rbxrequests carregado!")
        
        guild = discord.Object(id=SERVER_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        print("Comandos sincronizados no servidor!")
        
    async def on_ready(self):
        await self.change_presence(
            status=discord.Status.idle,
            activity=discord.Streaming(name="Roblox Group", url="https://www.twitch.tv/discord")
        )
        print(f"O bot {self.user} iniciou!!")

bot = LauncherBot()
bot.run(DISCORD_TOKEN)
