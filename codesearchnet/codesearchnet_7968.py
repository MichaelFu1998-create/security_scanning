def xml_extract_date(node, xpath, date_format='%d/%m/%Y'):
    """
    :param node: the node to be queried
    :param xpath: the path to fetch the child node that has the wanted date
    """
    return datetime.strptime(xml_extract_text(node, xpath), date_format)