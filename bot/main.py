import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from typing import Final
from tabulate import tabulate
from format.custom_table import thick_line
from queries import query_margin_recent, fuzzy_lookup_item_by_name
from player.highscores import fetch_highscores

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")


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
    await ctx.send(formatted_table)


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
