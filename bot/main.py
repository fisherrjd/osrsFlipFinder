import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from typing import Final
from tabulate import tabulate
from format.custom_table import thick_line

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is Online")

## TODO 
# !help (List commands available)
# !info {item name}
# !lookup {username}
# !margin {min margin}
# !profile - DEFINE STILL - fink docs? 


items = [
    ["Wine of zamorak", 800, 798, 2, "1.09M"],
    ["Maple longbow", 277, 275, 2, "2.01M"],
    ["Harralander potionas…", 785, 783, 2, "767.99K"],
    ["Mithril seeds", 945, 943, 2, "395.44K"],
    ["Grimy tarromin", 419, 417, 2, "671.34K"],
]

# Headers
headers = ["Name", "InstaBuy", "InstaSell", "Margin", "Volume"]

# Generate the table with the custom format
table = tabulate(items, headers, tablefmt=thick_line)

@bot.command()
async def poop(ctx):
    formatted_table = f"```{table}```"
    embed = discord.Embed(
    title="Item Table",
    description=formatted_table,
    color=discord.Color.blue()
    )
    await ctx.send(formatted_table)
    
# Print the table
print(table)


bot.run(TOKEN)
