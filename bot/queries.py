import datetime
import sqlite3
from collections import namedtuple

from fuzzywuzzy import process

from data_collection.utils.format import format_price
from data_collection.utils.time import humanize_time, calc_time_range

Item = namedtuple(
    "Item", ["name", "low", "low_time", "high", "high_time", "margin", "volume"]
)


def query_margin_recent(limit):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("data_collection/osrs_prices.db")
    cursor = conn.cursor()

    # Define a named tuple for the item structure

    # Calculate time window
    ten_minutes_ago = calc_time_range(10)
    # Query to fetch items with the largest margins
    cursor.execute(
        """
        SELECT Item_name,
               low,
               low_time,
               high,
               high_time,
               margin,
               volume
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
            volume=format_price(row[6]),
        )
        for row in rows
    ]


def fuzzy_lookup_item_by_name(item_name):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("data_collection/osrs_prices.db")
    cursor = conn.cursor()

    # Close the connection
    conn.close()
    return "WIP"


def flip_search(max_price, min_volume, time_range_minutes):

    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("data_collection/osrs_prices.db")
    cursor = conn.cursor()

    # Define a named tuple for the item structure

    # Calculate time window
    calc_range = calc_time_range(time_range_minutes)

    # Query to fetch items with the largest margins
    cursor.execute(
        """
        SELECT Item_name,
               low,
               low_time,
               high,
               high_time,
               margin,
               volume
        FROM item_prices
        WHERE high_time >= ?
        AND low_time >= ?
        AND volume >= ?
        AND high <= ?
        ORDER BY margin DESC
        LIMIT ?
    """,
        (calc_range, calc_range, min_volume, max_price, 5),
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
            volume=format_price(row[6]),
        )
        for row in rows
    ]
