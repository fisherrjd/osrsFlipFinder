import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from typing import Final
from player.highscores import fetch_highscores
from data_collection.info import lookup_item
from tabulate import tabulate
from format.custom_table import custom_tablefmt

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is Online")

import discord


    
## TODO 
# Write command to print items in table format from the DB


bot.run(TOKEN)
