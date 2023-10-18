def _default_json_default(obj):
    """ Coerce everything to strings.
    All objects representing time get output according to default_date_fmt.
    """
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.strftime(default_date_fmt)
    else:
        return str(obj)