from datetime import datetime
import time


class item:
    def __init__(
        self, id: int, highPrice: int, highTime: int, lowPrice: int, lowTime: int
    ) -> None:

        # TODO
        # self.name = name
        self.id = id
        self.highPrice = "{:,}".format(highPrice)
        self.highTime = datetime.utcfromtimestamp(time.time() - highTime).strftime(
            "%M minutes and %S seconds ago"
        )
        self.lowPrice = "{:,}".format(lowPrice)
        self.lowTime = datetime.utcfromtimestamp(time.time() - lowTime).strftime(
            "%M minutes and %S seconds ago"
        )
        self.margin = "{:,}".format(int(highPrice - lowPrice - highPrice * 0.01))

    # TODO
    # def get_name(self) -> str:
    #     return self.name

    def get_id(self) -> int:
        return self.id

    def get_high_price(self) -> str:
        return self.highPrice

    def get_high_time(self) -> str:
        return self.highTime

    def get_low_price(self) -> str:
        return self.lowPrice

    def get_low_time(self) -> str:
        return self.lowTime

    def get_margin(self) -> str:
        return self.margin
