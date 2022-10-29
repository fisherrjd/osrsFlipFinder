from contextlib import nullcontext
import requests
from osrsreboxed import items_api


ITEMS = items_api.load()
URL = "https://prices.runescape.wiki/api/v1/osrs/latest"
HEADERS = {
    "User-Agent": "@PapaBear#2007",
    "From": "fisherrjd@gmail.com",  # This is another valid field
}


class Item_list:
    def __init__(self) -> None:

        response = requests.get(URL, headers=HEADERS)
        data = response.json()
        self.price_data = data["data"]

    @property
    def item_obj(self) -> dict:
        return self.price_data

    def filter_by_margin(self, int: base_margin) -> dict:

        return null
