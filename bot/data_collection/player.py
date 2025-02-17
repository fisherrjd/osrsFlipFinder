import sqlite3

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
            item_list TEXT DEFAULT "[]"
        );
        """
    )

    conn.commit()
    conn.close()


def check_player_exists(discord_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 1 
        FROM players 
        WHERE discord_id = ?
        """,
        (discord_id,),
    )
    result = cursor.fetchone()
    conn.close()
    return result


def get_player_items(discord_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT item_list 
        FROM players 
        WHERE discord_id = ?
        """,
        (discord_id,),
    )
    result = cursor.fetchone()
    conn.close()
    return result


def main():
    conn = sqlite3.connect(DB_FILE)
    initialize_database(conn)


if __name__ == "__main__":
    main()
