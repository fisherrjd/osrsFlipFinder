import requests
from osrsreboxed import items_api
from utils.time import humanize_time
from utils.text import format_price
from utils.tax import calc_margin

ITEMS = items_api.load()
URL = "https://prices.runescape.wiki/api/v1/osrs/latest?id="
HEADERS = {
    "User-Agent": "@PapaBear#2007",
    "From": "fisherrjd@gmail.com",  # This is another valid field
}


class Item:
    def __init__(self, id: int) -> None:

        url = f"{URL}{id}"
        # print("fetching URL", url)
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        price_data = data["data"][f"{id}"]

        self.id = id
        self._item = ITEMS.lookup_by_item_id(self.id)
        self.high_price = format_price(price_data["high"])
        self.highTime = humanize_time(price_data["highTime"])
        self.low_price = format_price(price_data["low"])
        self.lowTime = humanize_time(price_data["lowTime"])
        self.margin = format_price(calc_margin(price_data["high"], price_data["low"]))

    def __repr__(self) -> str:
        return f"<Item[{self.id}]:{self.name}>"

    @property
    def name(self) -> str:
        return self._item.name

    @property
    def item_obj(self) -> dict:
        return {
            "Name": self.name,
            "id": self.id,
            "High Price": self.high_price,
            "Low Price": self.low_price,
            "Margin": self.margin,
            "High Time": self.highTime,
            "Low Time": self.lowTime,
        }
