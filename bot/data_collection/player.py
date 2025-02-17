import sqlite3
import json

DB_FILE = "players.db"


def initialize_database(conn):
    """Initialize or update the database schema."""
    cursor = conn.cursor()

    # Create the table if it does not exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS players (
            discord_id INTEGER PRIMARY KEY,
            discord_username TEXT DEFAULT "None",
            item_list TEXT DEFAULT "{}"
        );
        """
    )

    conn.commit()


def main():
    conn = sqlite3.connect(DB_FILE)
    initialize_database(conn)
    conn.close()


if __name__ == "__main__":
    main()
