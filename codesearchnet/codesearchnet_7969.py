def xml_extract_datetime(node, xpath, datetime_format='%d/%m/%Y %H:%M:%S'):
    """
    :param node: the node to be queried
    :param xpath: the path to fetch the child node that has the wanted datetime
    """
    return datetime.strptime(xml_extract_text(node, xpath), datetime_format)