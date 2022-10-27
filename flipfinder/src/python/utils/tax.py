def calc_margin(high: int, low: int) -> int:

    if high > 500000000:
        return 5000000
    else:
        return int(high - low - (high * 0.01))
