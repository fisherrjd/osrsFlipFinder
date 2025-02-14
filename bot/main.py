import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from typing import Final
from tabulate import tabulate
from format.custom_table import thick_line
import sqlite3
from collections import namedtuple
from data_collection.utils.time import humanize_time
from data_collection.utils.format import format_price
import datetime
from fuzzywuzzy import process

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

def query_margin_recent(limit):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('bot/data_collection/osrs_prices.db')
    cursor = conn.cursor()
    # Define a named tuple for the item structure
    Item = namedtuple('Item', ['name', 'low', 'low_time', 'high', 'high_time', 'margin'])

    current_time = int(datetime.datetime.now().timestamp())
    print(current_time)
    ten_minutes_ago = current_time - (10 * 60)
    # Query to fetch the top 5 items with the largest margins
    cursor.execute('''
        SELECT Item_name, low, low_time, high, high_time, margin 
        FROM item_prices 
        WHERE high_time >= ? AND low_time >= ?
        ORDER BY margin DESC 
        LIMIT ?
    ''', (ten_minutes_ago, ten_minutes_ago, limit))
    rows = cursor.fetchall()
    conn.close()

    # Convert rows into a list of named tuples
    return [Item(row[0], format_price(row[1]), humanize_time(row[2]), format_price(row[3]), humanize_time(row[4]), format_price(row[5])) for row in rows]
    



def fuzzy_lookup_item_by_name(item_name):
    conn = sqlite3.connect('bot/data_collection/osrs_prices.db')
    cursor = conn.cursor()
    threshold=70
    # Execute the SELECT query to find the item by name
    cursor.execute("SELECT item_name FROM item_prices")
    
    all_items = [row[0] for row in cursor.fetchall()]
    
    matches = process.extractBests(item_name, all_items, limit=5, score_cutoff=threshold)
        # Fetch the result
    matched_items = []
    for match, score in matches:
        cursor.execute("SELECT * FROM item_prices WHERE item_name = ?", (match,))
        matched_items.append(cursor.fetchone())
    # Close the connection
    conn.close()
    return matched_items




bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command("help")
@bot.event
async def on_ready():
    print("Bot is Online")

## TODO 
# !help
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
    items = query_margin_recent(limit)

    # Generate the table with the custom format
    table = tabulate(items, headers, tablefmt=thick_line)
    formatted_table = f"```{table}```"
    embed = discord.Embed(
    title="Item Table",
    description=formatted_table,
    color=discord.Color.blue()
    )
    await ctx.send(formatted_table)

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Bot Commands",
        description="List of available commands:",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="!top <number>",
        value="Displays the top items based on margin. Default is 5, max is 10.",
        inline=False
    )
    
    embed.add_field(
        name="!help",
        value="Shows this help message.",
        inline=False
    )

    await ctx.send(embed=embed)

@bot.command()
async def item(ctx, *, item_name):
            
    # Table Headers
    headers = ["Name", "Insta Buy", "Buy Time", "Insta Sell", "Sell Time", "Margin"]
    await ctx.send(f"Searching for item: **{item_name}**")
    # grab items from DB
    items = fuzzy_lookup_item_by_name(item_name)

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
