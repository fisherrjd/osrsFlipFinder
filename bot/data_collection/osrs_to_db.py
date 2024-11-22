import requests
import sqlite3
import time
from utils.tax import calc_margin
from utils.time import humanize_time

# Define the API URLs
LATEST_API_URL = "https://prices.runescape.wiki/api/v1/osrs/latest"
MAPPING_API_URL = "https://prices.runescape.wiki/api/v1/osrs/mapping"
HEADERS = {
    "User-Agent": "@PapaBear#2007",
    "From": "fisherrjd@gmail.com",  # This is another valid field
}
# SQLite database file
DB_FILE = "osrs_prices.db"

def initialize_database(conn):
    """Initialize or update the database schema."""
    cursor = conn.cursor()
    
    # Check and add columns if they don't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS item_prices (
        item_id INTEGER PRIMARY KEY
    );
    """)
    
    # List of columns to potentially add
    columns = [
        ('item_name', 'TEXT DEFAULT "Unknown"'),
        ('high', 'INTEGER DEFAULT 0'),
        ('highTime', 'INTEGER DEFAULT 0'),
        ('low', 'INTEGER DEFAULT 0'),
        ('lowTime', 'INTEGER DEFAULT 0'),
        ('margin', 'INTEGER DEFAULT 0')
    ]
    
    for column, dtype in columns:
        try:
            cursor.execute(f"ALTER TABLE item_prices ADD COLUMN {column} {dtype};")
        except sqlite3.OperationalError:
            # Column already exists
            pass
    
    conn.commit()

def fetch_data(api_url):
    """Fetch data from the given API."""
    response = requests.get(api_url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def process_mapping_data(mapping_data):
    """Process mapping data to create a dictionary of item_id -> name."""
    name_mapping = {}
    for item in mapping_data:
        item_id = str(item.get('id', ''))
        name = item.get('name', 'Unknown')
        if item_id:
            name_mapping[item_id] = name
    return name_mapping

def save_to_db(prices_data, name_mapping, db_file):
    """Save the fetched data into an SQLite database."""
    conn = sqlite3.connect(db_file)
    
    # Initialize database schema
    initialize_database(conn)
    
    cursor = conn.cursor()
    
    # Insert or update item prices and names
    for item_id, prices in prices_data.get('data', {}).items():
        # Safely extract values with defaults
        name = name_mapping.get(item_id, 'Unknown')
        high = prices.get('high', 0) or 0
        high_time = humanize_time(prices.get('highTime', 0) or 0)
        low = prices.get('low', 0) or 0
        low_time = humanize_time(prices.get('lowTime', 0) or 0)
        
        # Calculate margin using imported function
        margin = calc_margin(high, low)
        
        # Insert or update the item data
        cursor.execute(
            """
            INSERT INTO item_prices (item_id, item_name, high, highTime, low, lowTime, margin)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(item_id)
            DO UPDATE SET
                item_name = excluded.item_name,
                high = excluded.high,
                highTime = excluded.highTime,
                low = excluded.low,
                lowTime = excluded.lowTime,
                margin = excluded.margin
            """,
            (item_id, name, high, high_time, low, low_time, margin),
        )
    
    conn.commit()
    conn.close()

def main():
    """Main function to fetch data and save to the database every minute."""
    try:
        # Fetch item mapping data (item_id to name)
        mapping_data = fetch_data(MAPPING_API_URL)
        
        # Fetch the latest item prices
        latest_data = fetch_data(LATEST_API_URL)
        
        # Process the mapping data into a dictionary of item_id -> name
        name_mapping = process_mapping_data(mapping_data)
        
        # Save the data to the database
        save_to_db(latest_data, name_mapping, DB_FILE)
        print("Data saved successfully!")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)  # Wait for 60 seconds before running again