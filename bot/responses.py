from random import choice, randint
from data_collection.info import lookup_item

# Simulating a function that fetches the margin for an item
def get_info(item_name: str) -> str:
    return lookup_item(item_name)

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if '!info' in lowered:
        # Extract item_name from input after '!info'
        try:
            item_name = user_input.split('!info ')[1].strip()
            if item_name:
                # Call the get_info function and pass the item_name
                margin_info = get_info(item_name)
                return margin_info
            else:
                return 'Please provide a valid item_name after !info.'
        except IndexError:
            return 'Please provide an item_name after !info.'

