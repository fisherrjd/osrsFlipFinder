import sqlite3

def lookup_item(item_name: str) -> str:
    """Fetch item info from the database based on the item name."""
    
    # Connect to SQLite database
    conn = sqlite3.connect("data_collection/osrs_prices.db")
    cursor = conn.cursor()
    
    # Query for all columns where the item name matches
    cursor.execute("SELECT item_id, item_name, high, low, highTime, lowTime, margin FROM item_prices WHERE item_name LIKE ?", ('%' + item_name + '%',))
    items = cursor.fetchall()
    conn.close()
    
    # Check if there are items in the result
    if not items:
        return f"❌ **No items found** with `{item_name}` in the name. Please check your spelling or try a different search."

    # Return formatted results with flair
    result = "\n\n".join(
        [f"**🔹 {name}** (ID: {item_id})\n"
         f"**💰 High Price:** `{high}` GP (Last updated: {highTime})\n"
         f"**💸 Low Price:** `{low}` GP (Last updated: {lowTime})\n"
         f"**📊 Margin:** `{margin}` GP\n"
         f"```diff\n{'-' * 50}\n```"
         for item_id, name, high, low, highTime, lowTime, margin in items]
    )
    
    return result
