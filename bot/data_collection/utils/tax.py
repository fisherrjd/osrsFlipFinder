def calc_margin(high: int, low: int) -> int:
    """Calculates the GE tax for items to flip on OSRS

    Args:
        high: Price to Sell Item At
        low: Price to Buy Item At

    Returns:
        returns the calculated margin for "flipping" an item at the listed price
    Notes:
        - GE tax rate is 2.0% as of the latest update.
        - Items under 50 GP are not taxed.
        - Tax is capped at 5,000,000 coins.
    """

    if high < 50:
        tax = 0
    else:
        tax = int(high * 0.02)
        if tax > 5000000:
            tax = 5000000

    return int(high - low - tax)
