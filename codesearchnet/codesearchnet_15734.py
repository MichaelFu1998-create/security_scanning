def day_of_week(abbr=False):
    """Return a random (abbreviated if `abbr`) day of week name."""
    if abbr:
        return random.choice(DAYS_ABBR)
    else:
        return random.choice(DAYS)