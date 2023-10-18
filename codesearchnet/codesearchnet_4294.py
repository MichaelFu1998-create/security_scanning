def datetime_from_iso_format(string):
    """
    Return a datetime object from an iso 8601 representation.
    Return None if string is non conforming.
    """
    match = DATE_ISO_REGEX.match(string)
    if match:
        date = datetime.datetime(year=int(match.group(DATE_ISO_YEAR_GRP)),
                                 month=int(match.group(DATE_ISO_MONTH_GRP)),
                                 day=int(match.group(DATE_ISO_DAY_GRP)),
                                 hour=int(match.group(DATE_ISO_HOUR_GRP)),
                                 second=int(match.group(DATE_ISO_SEC_GRP)),
                                 minute=int(match.group(DATE_ISO_MIN_GRP)))
        return date
    else:
        return None