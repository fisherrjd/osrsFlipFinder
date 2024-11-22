import sqlite3
from data_collection.utils.format import format_price

def get_margin(margin: int) -> dict:
    """Fetch item info from the database based on the item name."""
    conn = sqlite3.connect("data_collection/osrs_prices.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT item_id, item_name, high, low, highTime, lowTime, margin FROM item_prices WHERE item_name LIKE ?",
        ('%' + margin + '%',)
    )
    items = cursor.fetchall()
    conn.close()

    if not items:
        return {"error": f"❌ **No items found** with `{margin}` in the name. Please check your spelling or try a different search."}

    return {
        "items": [
            {
                "item_id": item_id,
                "item_name": name,
                "high": format_price(high),
                "low": format_price(low),
                "highTime": highTime,
                "lowTime": lowTime,
                "margin": format_price(margin)
            }
            for item_id, name, high, low, highTime, lowTime, margin in items[:1]
        ]
    }
