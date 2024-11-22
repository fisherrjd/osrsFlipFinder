import discord
import sqlite3

async def get_margin(min_margin: int) -> discord.Embed:
    """Fetch items with a margin greater than the specified value and format as a rich embed."""

    # Connect to SQLite database
    conn = sqlite3.connect("data_collection/osrs_prices.db")
    cursor = conn.cursor()

    # Query items with margin greater than X
    cursor.execute(
        "SELECT item_id, item_name, high, low, highTime, lowTime, margin FROM item_prices WHERE margin > ?",
        (min_margin,),
    )
    items = cursor.fetchall()
    conn.close()

    # Check if any items match the criteria
    if not items:
        return discord.Embed(
            title="❌ No items found",
            description=f"No items found with a margin greater than `{min_margin}` GP.",
            color=discord.Color.red(),
        )

    # Create the embed object
    embed = discord.Embed(
        title=f"Items with Margin Greater than {min_margin} GP",
        description="Below are the items that meet your criteria.",
        color=discord.Color.green(),
    )

    # Build the table in the embed with fields for each row
    for item_id, name, high, low, highTime, lowTime, margin in items:
        embed.add_field(
            name=name[:50],  # truncate name if it's too long
            value=(
                f"**High:** {high} GP\n"
                f"**Low:** {low} GP\n"
                f"**Margin:** {margin} GP\n"
                f"**High Time:** {highTime}\n"
                f"**Low Time:** {lowTime}"
            ),
            inline=False
        )

    return embed
