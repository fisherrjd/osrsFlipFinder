# main.py

from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel
from typing import Final
import os
from dotenv import load_dotenv
from tabulate import tabulate

# Import your custom modules
from format.custom_table import thick_line
from player.highscores import fetch_highscores
from queries import query_margin_recent, fuzzy_lookup_item_by_name, flip_search
from data_collection.utils.format import parse_shorthand

# Load environment variables
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")  # Not used here but kept if needed later

# Item Info Table Headers
Item_Info_Headers = [
    "Name",
    "Insta Buy",
    "Buy Time",
    "Insta Sell",
    "Sell Time",
    "Margin",
    "24h Volume",
]

app = FastAPI(title="GameBot API", description="REST API version of the Discord bot")

# Models for request bodies
class FlipRequest(BaseModel):
    max_buy_price: str = "2147483647"
    min_volume: int = 1000
    time_range_minutes: int = 10


@app.get("/")
def read_root():
    return {"message": "Bot is Online"}


@app.get("/top")
def get_top(limit: int = 5):
    if limit > 10:
        limit = 10
    items = query_margin_recent(limit)
    table = tabulate(items, Item_Info_Headers, tablefmt=thick_line)
    return {"table": f"```\n{table}\n```", "items": items}


@app.get("/item/{item_name}")
def get_item(item_name: str):
    result = fuzzy_lookup_item_by_name(item_name)
    if not result:
        raise HTTPException(status_code=404, detail="No results found")
    table = tabulate(result, Item_Info_Headers, tablefmt=thick_line)
    return {"table": f"```\n{table}\n```", "results": result}


@app.get("/player/{username}")
def get_player(username: str):
    result = fetch_highscores(username)
    return {"result": result}


@app.post("/flip")
def post_flip(flip_data: FlipRequest):
    try:
        max_price = parse_shorthand(flip_data.max_buy_price)
        result = flip_search(max_price, flip_data.min_volume, flip_data.time_range_minutes)
        if not result:
            return {"message": "No Results...", "results": []}
        table = tabulate(result, Item_Info_Headers, tablefmt=thick_line)
        return {"table": f"```\n{table}\n```", "results": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error parsing input: {e}")


# @app.get("/help")
# def get_help(command: Optional[str] = None):
#     commands_info = {
#         "top": {
#             "usage": "`GET /top?limit=5`",
#             "description": "Displays the top items by margin. The limit defaults to 5 and caps at 10.",
#         },
#         "item": {
#             "usage": "`GET /item/{item_name}`",
#             "description": "Searches for an item by name and displays its buy/sell margins.",
#         },
#         "flip": {
#             "usage": "`POST /flip` with JSON body {max_buy_price, min_volume, time_range_minutes}",
#             "description": "Searches for items based on the max buy price, minimum volume, and time range in minutes. Default values are max_buy_price=2147483647, min_volume=1000, time_range_minutes=10.",
#         },
#         "player": {
#             "usage": "`GET /player/{username}`",
#             "description": "Fetches highscore data for a player.",
#         }
#     }

#     if command:
#         cmd = command.lower()
#         if cmd not in commands_info:
#             raise HTTPException(status_code=404, detail=f"Command '{cmd}' not found")
#         return {"command": cmd, "info": commands_info[cmd]}
#     else:
#         return {"commands": list(commands_info.keys()), "usage": "Use ?command=name for details"}