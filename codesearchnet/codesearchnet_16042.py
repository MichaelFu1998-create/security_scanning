def _parse_document_id(elm_tree):
    """Given the parsed xml to an `ElementTree`,
    parse the id from the content.

    """
    xpath = '//md:content-id/text()'
    return [x for x in elm_tree.xpath(xpath, namespaces=COLLECTION_NSMAP)][0]