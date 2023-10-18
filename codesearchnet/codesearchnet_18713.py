def convert_date_from_iso_to_human(value):
    """Convert a date-value to the ISO date standard for humans."""
    try:
        year, month, day = value.split("-")
    except ValueError:
        # Not separated by "-". Space?
        try:
            year, month, day = value.split(" ")
        except ValueError:
            # What gives? OK, lets just return as is
            return value

    try:
        date_object = datetime(int(year), int(month), int(day))
    except TypeError:
        return value
    return date_object.strftime("%d %b %Y")