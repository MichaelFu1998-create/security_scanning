def validate_date(date_text):
    """Return True if valid, raise ValueError if not"""
    try:
        if int(date_text) < 0:
            return True
    except ValueError:
        pass

    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        pass

    raise ValueError('Dates must be negative integers or YYYY-MM-DD in the past.')