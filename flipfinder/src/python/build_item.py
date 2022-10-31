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


class BuildItem:
    def __init__(
        self, id: int, high: int, low: int, highTime: int, lowTime: int
    ) -> None:
        """build item off of id without call to specific item id api"""

        self.id = id
        self.wikiInfo = ITEMS.lookup_by_item_id(self.id)
        self.name = self.wikiInfo.name
        self.high_price = format_price(high)
        self.highTime = humanize_time(highTime)
        self.low_price = format_price(low)
        self.lowTime = humanize_time(lowTime)
        self.margin = format_price(calc_margin(high, low))

        print("finish item")

    def __repr__(self) -> str:
        return f"<Item[{self.id}]:{self.name}>"

    # @property
    # def name(self) -> str:
    #     return self._item.name

    @property
    def item_obj(self) -> dict:
        return {
            "Name": self.name,
            "id": self.id,
            "High_Price": self.high_price,
            "Low_Price": self.low_price,
            "Margin": self.margin,
            "High_Time": self.highTime,
            "Low_Time": self.lowTime,
        }
