import sqlite3


DB_FILE = "users.db"


def initialize_database(conn):
    """Initialize or update the database schema."""
    cursor = conn.cursor()

    # Check and add columns if they don't exist
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS item_prices (
        item_id INTEGER PRIMARY KEY
    );
    """
    )

    # List of columns to potentially add
    columns = [
        ("discord_id", 'TEXT DEFAULT "None"'),
        ("disord_username", 'TEXT DEFAULT "None"'),
    ]

    for column, dtype in columns:
        try:
            cursor.execute(f"ALTER TABLE item_prices ADD COLUMN {column} {dtype};")
        except sqlite3.OperationalError:
            # Column already exists
            pass

    conn.commit()


def main():
    conn = sqlite3.connect(DB_FILE)
    initialize_database(conn)
