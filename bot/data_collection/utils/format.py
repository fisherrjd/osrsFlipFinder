import re


def format_price(price: int) -> str:
    """add commas to numbers for readablity"""

    return "{:,}".format(price)


def parse_shorthand(value: str):
    """Parse shorthand values like 10k, 10m into actual numbers."""
    multipliers = {"k": 1000, "m": 1000000, "b": 1000000000}
    value = value.lower().strip()

    # Check if the value ends with a valid shorthand character (k, m, b)
    if re.match(r"^\d+([kmb])$", value):  # Match only numbers followed by k/m/b
        multiplier = value[-1]
        number = float(value[:-1])  # Remove the last character and convert to float
        return int(number * multipliers[multiplier])

    raise ValueError(f"Invalid shorthand format: {value}. Use 'k', 'm', or 'b'.")
