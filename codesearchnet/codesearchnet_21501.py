def json_struct_to_xml(json_obj, root, custom_namespace=None):
    """Converts a Open511 JSON fragment to XML.

    Takes a dict deserialized from JSON, returns an lxml Element.

    This won't provide a conforming document if you pass in a full JSON document;
    it's for translating little fragments, and is mostly used internally."""
    if isinstance(root, (str, unicode)):
        if root.startswith('!'):
            root = etree.Element('{%s}%s' % (NS_PROTECTED, root[1:]))
        elif root.startswith('+'):
            if not custom_namespace:
                raise Exception("JSON fields starts with +, but no custom namespace provided")
            root = etree.Element('{%s}%s' % (custom_namespace, root[1:]))
        else:
            root = etree.Element(root)
    if root.tag in ('attachments', 'grouped_events', 'media_files'):
        for link in json_obj:
            root.append(json_link_to_xml(link))
    elif isinstance(json_obj, (str, unicode)):
        root.text = json_obj
    elif isinstance(json_obj, (int, float)):
        root.text = unicode(json_obj)
    elif isinstance(json_obj, dict):
        if frozenset(json_obj.keys()) == frozenset(('type', 'coordinates')):
            root.append(geojson_to_gml(json_obj))
        else:
            for key, val in json_obj.items():
                if key == 'url' or key.endswith('_url'):
                    el = json_link_to_xml(val, json_link_key_to_xml_rel(key))
                else:
                    el = json_struct_to_xml(val, key, custom_namespace=custom_namespace)
                if el is not None:
                    root.append(el)
    elif isinstance(json_obj, list):
        tag_name = root.tag
        if tag_name.endswith('ies'):
            tag_name = tag_name[:-3] + 'y'
        elif tag_name.endswith('s'):
            tag_name = tag_name[:-1]
        for val in json_obj:
            el = json_struct_to_xml(val, tag_name, custom_namespace=custom_namespace)
            if el is not None:
                root.append(el)
    elif json_obj is None:
        return None
    else:
        raise NotImplementedError
    return root