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
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")


def query_margin_recent(limit):
    """
    Query the database for items with the largest margins in the last 10 minutes.

    Args:
        limit (int): Maximum number of items to return

    Returns:
        list[Item]: List of items with their prices and margins, sorted by margin descending
    """
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("bot/data_collection/osrs_prices.db")
    cursor = conn.cursor()

    # Define a named tuple for the item structure
    Item = namedtuple(
        "Item", ["name", "low", "low_time", "high", "high_time", "margin"]
    )

    # Calculate time window
    current_time = int(datetime.datetime.now().timestamp())
    ten_minutes_ago = current_time - (10 * 60)

    # Query to fetch items with the largest margins
    cursor.execute(
        """
        SELECT Item_name,
               low,
               low_time,
               high,
               high_time,
               margin
        FROM item_prices
        WHERE high_time >= ?
        AND low_time >= ?
        ORDER BY margin DESC
        LIMIT ?
    """,
        (ten_minutes_ago, ten_minutes_ago, limit),
    )

    rows = cursor.fetchall()
    conn.close()

    # Convert rows into a list of named tuples with formatted values
    return [
        Item(
            name=row[0],
            low=format_price(row[1]),
            low_time=humanize_time(row[2]),
            high=format_price(row[3]),
            high_time=humanize_time(row[4]),
            margin=format_price(row[5]),
        )
        for row in rows
    ]


def fuzzy_lookup_item_by_name(item_name):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("bot/data_collection/osrs_prices.db")
    cursor = conn.cursor()

    # Define a named tuple for the item structure
    Item = namedtuple(
        "Item", ["name", "low", "low_time", "high", "high_time", "margin"]
    )

    # Execute the SELECT query to get all item names
    cursor.execute("SELECT item_name FROM item_prices")
    all_items = [row[0] for row in cursor.fetchall()]

    # Find fuzzy matches with a score cutoff of 70
    matches = process.extractBests(item_name, all_items, score_cutoff=70)

    # Fetch the complete data for matched items
    matched_items = []
    for match, score in matches:
        cursor.execute(
            """
            SELECT Item_name, low, low_time, high, high_time, margin
            FROM item_prices 
            WHERE item_name = ?
        """,
            (match,),
        )
        row = cursor.fetchone()
        if row:
            matched_items.append(
                Item(
                    row[0],
                    format_price(row[1]),
                    humanize_time(row[2]),
                    format_price(row[3]),
                    humanize_time(row[4]),
                    format_price(row[5]),
                )
            )

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
        title="Item Table", description=formatted_table, color=discord.Color.blue()
    )
    await ctx.send(formatted_table)


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
        title="Item Table", description=formatted_table, color=discord.Color.blue()
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
import discord


@bot.command()
async def help(ctx, command_name: str = None):
    """Displays a list of available commands or detailed help for a specific command."""

    commands_info = {
        "top": {
            "usage": "`!top [limit]`",
            "description": "Displays the top items by margin. The limit defaults to 5 and caps at 10.",
        },
        "item": {
            "usage": "`!item <item_name>`",
            "description": "Searches for an item by name and displays its buy/sell margins.",
        },
    }

    if command_name:
        command_name = command_name.lower()
        if command_name in commands_info:
            cmd_info = commands_info[command_name]
            embed = discord.Embed(
                title=f"Help: `{command_name}`", color=discord.Color.blue()
            )
            embed.add_field(name="Usage", value=cmd_info["usage"], inline=False)
            embed.add_field(
                name="Description", value=cmd_info["description"], inline=False
            )
            embed.set_footer(text="Use !help to see all available commands.")
            await ctx.send(embed=embed)
        else:
            await ctx.send(
                f"❌ Command `{command_name}` not found. Use `!help` to see available commands."
            )
    else:
        embed = discord.Embed(
            title="📖 Bot Commands",
            description="Here is a list of available commands. Use `!help <command>` for details.",
            color=discord.Color.green(),
        )

        for cmd, info in commands_info.items():
            embed.add_field(name=f"🔹 `{cmd}`", value=info["description"], inline=False)

        embed.set_footer(text="Use !help <command> for more details.")
        await ctx.send(embed=embed)


bot.run(TOKEN)
