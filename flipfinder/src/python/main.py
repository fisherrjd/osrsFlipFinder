import requests
from item import Item
from fastapi import FastAPI

URL = "https://prices.runescape.wiki/api/v1/osrs/latest?id="
HEADERS = {
    "User-Agent": "@PapaBear#2007",
    "From": "fisherrjd@gmail.com",  # This is another valid field
}
APP = FastAPI()


@APP.get("/item/{item_id}")
def get_item_data(item_id: int) -> object:
    """run a get request with our default headers"""
    url = f"{URL}{item_id}"
    # print("fetching URL", url)
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    price_data = data["data"][f"{item_id}"]
    temp = Item(
        item_id,
        price_data["high"],
        price_data["highTime"],
        price_data["low"],
        price_data["lowTime"],
    )
    return {"item": temp.item_obj}
