from item import Item
from fastapi import FastAPI
from utils.item_list import Item_list


# create a database file

APP = FastAPI()


@APP.get("/item/{item_id}")
def get_item_data(item_id: int) -> object:
    """run a get request with our default headers"""

    temp = Item(item_id)
    return {"item1": [temp.item_obj]}


@APP.get("/margin")
def get_margin_over_1m() -> dict:
    """run request to get all item margins over 1m"""

    temp = Item_list()
    return {"test": temp.id_list}


# TODO
# cache data locally- local database -sqllite?
# chron timer input to a database
# disk lookups
#
#
