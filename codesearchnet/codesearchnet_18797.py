def print_recs(listofrec, format=1, tags=None):
    """
    Print a list of records.

    :param format: 1 XML, 2 HTML (not implemented)
    :param tags: list of tags to be printed
           if 'listofrec' is not a list it returns empty string
    """
    if tags is None:
        tags = []
    text = ""

    if type(listofrec).__name__ != 'list':
        return ""
    else:
        for rec in listofrec:
            text = "%s\n%s" % (text, print_rec(rec, format, tags))
    return text