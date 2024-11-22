import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from typing import Final
from player.highscores import fetch_highscores
from data_collection.info import lookup_item

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is Online")

import discord

@bot.command(aliases=['highscores', 'lu'])
async def lookup(ctx, username: str):
    """Fetch and display OSRS Highscores data."""
    await ctx.send("Fetching User data...")
    result = fetch_highscores(username)

    if "error" in result:
        await ctx.send(result["error"])
    else:
        # Create an embed object
        embed = discord.Embed(
            title=f"**{result['username']}**'s OSRS Highscores", 
            color=discord.Color.blurple()
        )

        # Get skills from the result and sort them by skill name
        skills = result.get('skills', {})
        sorted_skills = sorted(skills.items(), key=lambda x: x[0])

        # Define a consistent width for the skill names and levels
        max_skill_length = max(len(skill) for skill, _ in sorted_skills)
        max_level_length = 3  # Levels are 3 digits (e.g., 99)

        # Prepare the skill display as a monospaced text (e.g., 'skill_name level')
        skill_str = ""
        skill_count = 0

        # Add skills in sets of 3
        for skill, data in sorted_skills:
            # Create the formatted line with padding for the skill names and levels
            skill_line = f"{skill.ljust(max_skill_length)} {str(data['level']).rjust(max_level_length)}"
            skill_str += skill_line

            # Add a pipe separator, but skip the last one
            if skill_count % 3 == 2:
                skill_str += "\n"
            else:
                skill_str += " | "

            skill_count += 1

        # Handle case where the last line is not filled with 3 skills
        if len(sorted_skills) % 3 != 0:
            skill_str = skill_str.rstrip(" |")  # Remove trailing pipe if any

        # Add skills to the embed as monospaced text
        embed.add_field(name="Skills", value=f"```{skill_str}```", inline=False)

        # Send the embed
        await ctx.send(embed=embed)


@bot.command()
async def info(ctx, *, item_name: str):
    """Fetch and display item information with an embedded message."""
    await ctx.send("Fetching item data...")
    result = lookup_item(item_name)

    if "error" in result:
        await ctx.send(result["error"])
        return

    # Embed creation
    embed = discord.Embed(
        title=f"Search Results for '{item_name}'",
        description="Here are the top matches from the database:",
        color=0x3498db  # Optional: color of the embed
    )
    embed.set_footer(text="Refine your search for more specific results.")

    # Add fields for each item (limit to 5 items in lookup_item)
    for item in result["items"]:
        embed.add_field(
            name=f"🔹 {item['item_name']} (ID: {item['item_id']})",
            value=(
                f"**💰 Insta Buy Price:** `{item['high']} GP`\n"
                f"**💸 Insta Sell Price:** `{item['low']} GP`\n"
                f"**📊 Margin:** `{item['margin']} GP`\n"
                f"Last Updated: `{item['highTime']}`"
            ),
            inline=False  # Inline means multiple fields in one row; False stacks them
        )

    # Send the embed
    await ctx.send(embed=embed)


bot.run(TOKEN)
