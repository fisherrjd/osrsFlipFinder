import os
from typing import Final

import discord
from discord.ext import commands
from dotenv import load_dotenv
from tabulate import tabulate

from format.custom_table import thick_line
from player.highscores import fetch_highscores
from queries import query_margin_recent, fuzzy_lookup_item_by_name, flip_search
from data_collection.utils.format import parse_shorthand

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
Item_Info_Headers = [
    "Name",
    "Insta Buy",
    "Buy Time",
    "Insta Sell",
    "Sell Time",
    "Margin",
    "24h Volume",
]


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


# !top X
@bot.command()
async def top(ctx, limit: int = 5):
    # Cap the limit at 10
    if limit > 10:
        limit = 10
        await ctx.send("The maximum limit is 10. Showing top 10 items.")

    # Table Headers

    # grab items from DB
    items = query_margin_recent(limit)

    # Generate the table with the custom format
    table = tabulate(items, Item_Info_Headers, tablefmt=thick_line)
    formatted_table = f"```{table}```"
    await ctx.send(formatted_table)


# !item
@bot.command()
async def item(ctx, *, item_name):
    if item_name == "unknown":
        await ctx.send("```No results found```")
    else:
        # Table Headers
        await ctx.send(f"Searching for item: **{item_name}**")
        # grab items from DB
        result = fuzzy_lookup_item_by_name(item_name)

        if result:
            # Generate the table with the custom format
            table = tabulate(result, Item_Info_Headers, tablefmt=thick_line)
            formatted_table = f"```{table}```"
            await ctx.send(formatted_table)
        else:
            await ctx.send("```No Results...```")


@top.error
async def top_error(ctx, error):
    # Handle invalid input (e.g., !top test)
    if isinstance(error, commands.BadArgument):
        await ctx.send("Incorrect usage: `!top <number>`")
    # Handle other unexpected errors
    else:
        await ctx.send(f"An error occurred: {error}")


# !player
@bot.command()
async def player(ctx, username):
    if username == "big16ind":
        await ctx.send("fuckin NERD")
    else:
        temp = fetch_highscores(username)
        await ctx.send(temp)


# !flip
# TODO:
# Implement better usage
#
@bot.command()
async def flip(
    ctx,
    max_buy_price: str = "2147483647",
    min_volume: int = 1000,
    time_range_minutes: int = 10,
):
    try:
        # Parse shorthand values
        max_price = parse_shorthand(max_buy_price)
        # Perform the search with parsed values
        result = flip_search(max_price, min_volume, time_range_minutes)

        if result:
            # Generate the table with the custom format
            table = tabulate(result, Item_Info_Headers, tablefmt=thick_line)
            formatted_table = f"```{table}```"
            await ctx.send(formatted_table)
        else:
            await ctx.send("```No Results...```")

    except ValueError as e:
        # Catch any ValueErrors thrown by parse_shorthand
        await ctx.send(
            f"❌ Error: {str(e)}. Please use shorthand notation like 10k, 10m, etc."
        )


# !help
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
        "flip": {
            "usage": "`!flip [max_buy_price] [min_volume] [time_range_minutes]`",
            "description": "Searches for items based on the max buy price, minimum volume, and time range in minutes. Default values are max_buy_price=2147483647, min_volume=1000, time_range_minutes=10.",
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
