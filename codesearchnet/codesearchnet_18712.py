def convert_date_to_iso(value):
    """Convert a date-value to the ISO date standard."""
    date_formats = ["%d %b %Y", "%Y/%m/%d"]
    for dformat in date_formats:
        try:
            date = datetime.strptime(value, dformat)
            return date.strftime("%Y-%m-%d")
        except ValueError:
            pass
    return value