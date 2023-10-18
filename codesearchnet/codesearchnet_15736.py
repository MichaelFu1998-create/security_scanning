def year(past=False, min_delta=0, max_delta=20):
    """Return a random year."""
    return dt.date.today().year + _delta(past, min_delta, max_delta)