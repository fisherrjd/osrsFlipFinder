from random import choice, randint
from data_collection.info import lookup_item
from data_collection.margin import get_margin

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

    if '!margin' in lowered:
        try:
            # Extract the minimum margin from input after '!margin'
            min_margin = user_input.split('!margin ')[1].strip()
            
            if min_margin.isdigit():
                min_margin = int(min_margin)
                
                # Call the get_margin function and pass the minimum margin
                margin_results = get_margin(min_margin)
                
                # If results exist, format and return them
                if margin_results:
                    # Return results joined as separate Discord messages
                    return "\n\n".join(margin_results)
                else:
                    return f"❌ No items found with a margin greater than `{min_margin}` GP."
            else:
                return "❌ Please provide a valid number after `!margin`."
        except IndexError:
            return "❌ Please provide a minimum margin value after `!margin`."
