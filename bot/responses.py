from random import choice, randint
from item import Item

# Simulating a function that fetches the margin for an item
def get_item_margin(item_id: str) -> str:

    temp = Item(item_id)
    return {"item": [temp.item_obj]}

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif '!info' in lowered:
        # Extract ITEM_ID from input after '!info'
        try:
            item_id = user_input.split('!info ')[1].strip()
            if item_id.isdigit():
                # Call the get_item_margin function and pass the ITEM_ID
                margin_info = get_item_margin(item_id)
                return margin_info
            else:
                return 'Invalid ITEM_ID format. Please provide a valid number.'
        except IndexError:
            return 'Please provide an ITEM_ID after !info.'
    else:
        return 'I didn\'t quite catch that. Could you rephrase?'
