def decode_html_entities(html):
    """
    Decodes a limited set of HTML entities.
    """
    if not html:
        return html

    for entity, char in six.iteritems(html_entity_map):
        html = html.replace(entity, char)

    return html