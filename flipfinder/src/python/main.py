from item import Item
from fastapi import FastAPI
from utils.item_list import Item_list
import sqlite3


# create a database file
CONNECTION = sqlite3.connect("Item_Data.sqlite")
CONNECTION.close()
APP = FastAPI()


@APP.get("/item/{item_id}")
def get_item_data(item_id: int) -> object:
    """run a get request with our default headers"""

    temp = Item(item_id)
    return {"item1": [temp.item_obj]}


# TODO
# cache data locally- local database -sqllite?
# chron timer input to a database
# disk lookups
#
#


@APP.get("/item/1m")
def get_margin_over_1m() -> dict:
    """run request to get all item margins over 1m"""

    temp = Item_list()

    return temp.item_obj
