def print_rec(rec, format=1, tags=None):
    """
    Print a record.

    :param format: 1 XML, 2 HTML (not implemented)
    :param tags: list of tags to be printed
    """
    if tags is None:
        tags = []
    if format == 1:
        text = record_xml_output(rec, tags)
    else:
        return ''

    return text