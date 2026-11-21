import os
import discord
import requests
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()
ROBLOX_TOKEN = os.getenv("ROBLOX_TOKEN")

GroupName = "Hello Studios"

def FormatPlural(days: int) -> str:
    if days is not None and days > 1:
        return "s"
    return ""

def TimerDetect(user_id):
    url = f"https://apis.roblox.com/cloud/v2/groups/689923286/memberships"
    
    headers = {
        "x-api-key": ROBLOX_TOKEN
    }
    
    params = {
        "filter": f"user == 'users/{user_id}'"
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        memberships = data.get("groupMemberships", [])
        
        if len(memberships) > 0:
            create_time_str = memberships[0]["createTime"]
            dataEntry = datetime.fromisoformat(create_time_str.replace("Z", "+00:00"))
            nowTime = datetime.now(timezone.utc)
            result = (nowTime - dataEntry).days
            return result
        else:
            return -1
    else:
        print(f"Error in API Roblox: {response.status_code} - {response.text}")
        return None

class RbxRequests(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        
    @app_commands.command(
        name="elegibilidade-grupo",
        description="Confira se você já pode receber pagamentos de Robux pelo nosso grupo."
    )
    @app_commands.describe(
        id="Insira o seu ID do Roblox."
    )
    async def grupo(self, interaction: discord.Interaction, id: int):
        await interaction.response.defer(ephemeral=True)

        if id == 0:
            await interaction.followup.send(f"Olá {interaction.user.mention}! Você precisa informar um ID válido.")
            return
            
        days = TimerDetect(id)
        letter = FormatPlural(days)

        if days is None:
            await interaction.followup.send(f"Olá {interaction.user.mention}! Ocorreu um erro ao consultar a API do Roblox. Tente novamente mais tarde.")
            return

        if days == -1:
            print(f"Discord: {interaction.user.name}, {interaction.user.id} / ID: {id} / não faz parte do grupo.")
            await interaction.followup.send(f"Olá {interaction.user.mention}! Infelizmente você não faz parte do grupo da {GroupName}.")
        
        elif days == 0:
            print(f"Discord: {interaction.user.name}, {interaction.user.id} / ID: {id} / entrou hoje!")
            await interaction.followup.send(f"Olá {interaction.user.mention}! Você ainda não pode receber pagamentos via grupo pois você entrou hoje.")
            
        elif days < 15:
            print(f"Discord: {interaction.user.name}, {interaction.user.id} / ID: {id} / está no grupo da {GroupName} há {days} dia{letter}!")
            await interaction.followup.send(f"Olá {interaction.user.mention}! Você ainda não pode receber pagamentos via grupo, você está no grupo há apenas {days} dia{letter}.")
            
        elif days >= 15:
            print(f"Discord: {interaction.user.name}, {interaction.user.id} / ID: {id} / está no grupo da {GroupName} há {days} dia{letter}!")
            await interaction.followup.send(f"Olá {interaction.user.mention}! Você já pode receber pagamentos via grupo! Você está no grupo da {GroupName} há {days} dia{letter}.")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(RbxRequests(client))