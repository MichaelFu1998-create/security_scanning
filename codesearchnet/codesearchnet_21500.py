def json_doc_to_xml(json_obj, lang='en', custom_namespace=None):
    """Converts a Open511 JSON document to XML.

    lang: the appropriate language code

    Takes a dict deserialized from JSON, returns an lxml Element.

    Accepts only the full root-level JSON object from an Open511 response."""
    if 'meta' not in json_obj:
        raise Exception("This function requires a conforming Open511 JSON document with a 'meta' section.")
    json_obj = dict(json_obj)
    meta = json_obj.pop('meta')
    elem = get_base_open511_element(lang=lang, version=meta.pop('version'))

    pagination = json_obj.pop('pagination', None)

    json_struct_to_xml(json_obj, elem, custom_namespace=custom_namespace)

    if pagination:
        elem.append(json_struct_to_xml(pagination, 'pagination', custom_namespace=custom_namespace))

    json_struct_to_xml(meta, elem)

    return elem