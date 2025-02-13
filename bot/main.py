import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from typing import Final
from tabulate import tabulate
from format.custom_table import thick_line
import sqlite3
from collections import namedtuple


load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

def query_margin():


# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('bot/data_collection/osrs_prices.db')
cursor = conn.cursor()
# Define a named tuple for the item structure
Item = namedtuple('Item', ['name', 'low', 'low_time', 'high', 'high_time', 'margin'])
# Query to fetch the top 5 items with the largest margins
cursor.execute('''
    SELECT Item_name, low, , lowTime, high, highTime, margin 
    FROM item_prices 
    ORDER BY margin DESC 
    LIMIT 5
''')
rows = cursor.fetchall()
# Convert rows into a list of named tuples
items = [Item(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]





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


# items = [
#     # ["name of item", low, high, margin]
#     ["Wine of zamorak", 800, 798, 2],
#     ["Maple longbow", 277, 275, 2],
#     ["Harralander potionas…", 785, 783, 2],
#     ["Mithril seeds", 945, 943, 2],
#     ["Grimy tarromin", 419, 417, 2],
# ]

# Headers
headers = ["Name", "Insta Buy", "Buy Time", "Insta Sell", "Sell Time", "Margin"]

# Generate the table with the custom format
table = tabulate(items, headers, tablefmt=thick_line)

@bot.command()
async def top5(ctx):
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
