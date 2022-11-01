def calc_margin(high: int, low: int) -> int:
    """calculate the margin of an item"""

    if high > 500000000:
        return 5000000
    else:
        return int(high - low - (high * 0.01))
