def ensure_format(doc, format):
    """
    Ensures that the provided document is an lxml Element or json dict.
    """
    assert format in ('xml', 'json')
    if getattr(doc, 'tag', None) == 'open511':
        if format == 'json':
            return xml_to_json(doc)
    elif isinstance(doc, dict) and 'meta' in doc:
        if format == 'xml':
            return json_doc_to_xml(doc)
    else:
        raise ValueError("Unrecognized input document")
    return doc