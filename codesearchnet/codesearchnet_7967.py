def xml_extract_text(node, xpath):
    """
    :param node: the node to be queried
    :param xpath: the path to fetch the child node that has the wanted text
    """
    text = node.find(xpath).text
    if text is not None:
        text = text.strip()
    return text