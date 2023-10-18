def date(past=False, min_delta=0, max_delta=20):
    """Return a random `dt.date` object. Delta args are days."""
    timedelta = dt.timedelta(days=_delta(past, min_delta, max_delta))
    return dt.date.today() + timedelta