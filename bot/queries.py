from fuzzywuzzy import process
import sqlite3
import datetime
from collections import namedtuple
from data_collection.utils.time import humanize_time
from data_collection.utils.format import format_price


def query_margin_recent(limit):
    """
    Query the database for items with the largest margins in the last 10 minutes.

    Args:
        limit (int): Maximum number of items to return

    Returns:
        list[Item]: List of items with their prices and margins, sorted by margin descending
    """
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("data_collection/osrs_prices.db")
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
    conn = sqlite3.connect("data_collection/osrs_prices.db")
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
