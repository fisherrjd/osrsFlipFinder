def calc_margin(high: int, low: int) -> int:
    """Calculates the GE tax for items to flip on OSRS

    Args:
        high: Price to Sell Item At
        low: Price to Buy Item At

    Returns:
        returns the calculated margin for "flipping" an item at the listed price
    """

    if high > 500000000:
        return int(high - low - (5000000))
    else:
        return int(high - low - (high * 0.01))
