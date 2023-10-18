def _datetime_to_utc_int(date):
    """Convert the integer UTC time value into a local datetime."""
    if date is None:
      return None

    # Convert localized datetime to a UTC integer
    epoch = dsub_util.replace_timezone(datetime.utcfromtimestamp(0), pytz.utc)
    return (date - epoch).total_seconds()