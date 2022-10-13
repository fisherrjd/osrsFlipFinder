import requests
from typing import Union
from items import ID
from item import item
from fastapi import FastAPI

URL = "https://prices.runescape.wiki/api/v1/osrs/latest?id="
HEADERS = {
    "User-Agent": "@PapaBear#2007",
    "From": "fisherrjd@gmail.com",  # This is another valid field
}
app = FastAPI()


@app.get("/")
def index():
    return "congrats its a webapp"


@app.get("/item/{item_id}")
def get_item_data(item_id: int) -> object:
    """run a get request with our default headers"""
    headers = HEADERS
    url = f"{URL}{item_id}"
    # print("fetching URL", url)
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    price_data = data["data"][f"{item_id}"]
    temp = item(
        item_id,
        price_data["high"],
        price_data["highTime"],
        price_data["low"],
        price_data["lowTime"],
    )
    return {
        "item_id": temp.get_id(),
        "item_high_price": temp.get_high_price(),
        "item_high_time": temp.get_high_time(),
        "item_low_price": temp.get_low_price(),
        "item_low_time": temp.get_low_time(),
    }
