def month(abbr=False, numerical=False):
    """Return a random (abbreviated if `abbr`) month name or month number if
    `numerical`.
    """
    if numerical:
        return random.randint(1, 12)
    else:
        if abbr:
            return random.choice(MONTHS_ABBR)
        else:
            return random.choice(MONTHS)