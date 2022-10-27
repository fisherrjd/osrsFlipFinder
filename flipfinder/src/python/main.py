from item import Item
from fastapi import FastAPI
from item_list import Item_list


APP = FastAPI()


@APP.get("/item/{item_id}")
def get_item_data(item_id: int) -> object:
    """run a get request with our default headers"""

    temp = Item(item_id)
    return {"item1": [temp.item_obj]}


@APP.get("/item/1m")
def get_margin_over_1m() -> list:
    """run request to get all item margins over 1m"""

    temp = Item_list()

    return temp.price_data
