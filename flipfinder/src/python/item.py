from osrsreboxed import items_api
from utils.time import humanize_time
from utils.text import format_price

ITEMS = items_api.load()


class Item:
    def __init__(
        self, id: int, high_price: int, highTime: int, low_price: int, lowTime: int
    ) -> None:

        self.id = id
        self._item = ITEMS.lookup_by_item_id(self.id)
        self.high_price = format_price(high_price)
        self.highTime = humanize_time(highTime)
        self.low_price = format_price(low_price)
        self.lowTime = humanize_time(lowTime)
        self.margin = format_price(int(high_price - low_price - high_price * 0.01))

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
