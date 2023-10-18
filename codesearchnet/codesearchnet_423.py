def to_utc(df):
    """
    For use in tests; applied UTC timestamp to DataFrame.
    """

    try:
        df.index = df.index.tz_localize('UTC')
    except TypeError:
        df.index = df.index.tz_convert('UTC')

    return df