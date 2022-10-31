import requests
from osrsreboxed import items_api
from build_item import BuildItem


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
        self.pog = data["data"]

        self.id_list = []
        for i in self.pog:
            if len(data["data"][i]) != 0:
                price_data = data["data"][i]

                if (
                    (price_data["high"]) is not None
                    and price_data["low"] is not None
                    and price_data["highTime"] is not None
                    and price_data["lowTime"] is not None
                    and int(i) < 27205
                ):
                    self.id_list.append(
                        BuildItem(
                            int(i),
                            price_data["high"],
                            price_data["low"],
                            price_data["highTime"],
                            price_data["lowTime"],
                        )
                    )
