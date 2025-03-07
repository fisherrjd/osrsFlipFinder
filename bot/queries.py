import datetime
import sqlite3
from collections import namedtuple

from fuzzywuzzy import process

from data_collection.utils.format import format_price
from data_collection.utils.time import humanize_time, calc_time_range

Item = namedtuple(
    "Item", ["name", "low", "low_time", "high", "high_time", "margin", "volume"]
)


def query_margin_recent(limit: int) -> list:
    """Lookup for "best" margins in the last 10 minutes with no other restricitons

    Args:
        limit: How many items to display

    Returns:
        returns list of "limit" items caps at 10
    """
    conn = sqlite3.connect("data_collection/osrs_prices.db")
    cursor = conn.cursor()

    ten_minutes_ago = calc_time_range(10)
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


def fuzzy_lookup_item_by_name(item_name: str) -> list:
    """_summary_

    Args:
        item_name: _description_

    Returns:
        _description_
    """
    conn = sqlite3.connect("data_collection/osrs_prices.db")
    cursor = conn.cursor()

    # Close the connection
    conn.close()
    return "WIP"


def flip_search(max_price: str, min_volume: int, time_range_minutes: int) -> list:
    """Adds additional parameters on the query margin research to enable better filtered results

    Args:
        max_price: Max buy price of items shown
        min_volume: Number of items traded in the last 24 hours
        time_range_minutes: how recently the item must have been traded

    Returns:
        Returns of list of items matching parameters
    """
    conn = sqlite3.connect("data_collection/osrs_prices.db")
    cursor = conn.cursor()

    calc_range = calc_time_range(time_range_minutes)

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
