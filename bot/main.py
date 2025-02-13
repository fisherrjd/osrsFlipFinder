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

def query_margin(limit):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('bot/data_collection/osrs_prices.db')
    cursor = conn.cursor()
    # Define a named tuple for the item structure
    Item = namedtuple('Item', ['name', 'low', 'low_time', 'high', 'high_time', 'margin'])
    # Query to fetch the top 5 items with the largest margins
    cursor.execute('''
        SELECT Item_name, low, low_time, high, high_time, margin 
        FROM item_prices 
        ORDER BY margin DESC 
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    # Convert rows into a list of named tuples
    return [Item(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]







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

@bot.command()
async def top(ctx, limit: int = 5):
    # Cap the limit at 10
    if limit > 10:
        limit = 10
        await ctx.send("The maximum limit is 10. Showing top 10 items.")
            
    # Table Headers
    headers = ["Name", "Insta Buy", "Buy Time", "Insta Sell", "Sell Time", "Margin"]

    # grab items from DB
    items = query_margin(limit)

    # Generate the table with the custom format
    table = tabulate(items, headers, tablefmt=thick_line)
    formatted_table = f"```{table}```"
    embed = discord.Embed(
    title="Item Table",
    description=formatted_table,
    color=discord.Color.blue()
    )
    await ctx.send(formatted_table)

@top.error
async def top_error(ctx, error):
    # Handle invalid input (e.g., !top test)
    if isinstance(error, commands.BadArgument):
        await ctx.send("Incorrect usage: `!top <number>`")
    # Handle other unexpected errors
    else:
        await ctx.send(f"An error occurred: {error}")

# Print the table
# print(table)


bot.run(TOKEN)
