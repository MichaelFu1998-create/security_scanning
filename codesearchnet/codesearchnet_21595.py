def xml_to_json(root):
    """Convert an Open511 XML document or document fragment to JSON.

    Takes an lxml Element object. Returns a dict ready to be JSON-serialized."""
    j = {}

    if len(root) == 0:  # Tag with no children, return str/int
        return _maybe_intify(root.text)

    if len(root) == 1 and root[0].tag.startswith('{' + NS_GML):  # GML
        return gml_to_geojson(root[0])

    if root.tag == 'open511':
        j['meta'] = {'version': root.get('version')}

    for elem in root:
        name = elem.tag
        if name == 'link' and elem.get('rel'):
            name = elem.get('rel') + '_url'
            if name == 'self_url':
                name = 'url'
            if root.tag == 'open511':
                j['meta'][name] = elem.get('href')
                continue
        elif name.startswith('{' + NS_PROTECTED):
            name = '!' + name[name.index('}') + 1:] 
        elif name[0] == '{':
            # Namespace!
            name = '+' + name[name.index('}') + 1:]

        if name in j:
            continue  # duplicate
        elif elem.tag == 'link' and not elem.text:
            j[name] = elem.get('href')
        elif len(elem):
            if name == 'grouped_events':
                # An array of URLs
                j[name] = [xml_link_to_json(child, to_dict=False) for child in elem]
            elif name in ('attachments', 'media_files'):
                # An array of JSON objects
                j[name] = [xml_link_to_json(child, to_dict=True) for child in elem]
            elif all((name == pluralize(child.tag) for child in elem)):
                # <something><somethings> serializes to a JSON array
                j[name] = [xml_to_json(child) for child in elem]
            else:
                j[name] = xml_to_json(elem)
        else:
            if root.tag == 'open511' and name.endswith('s') and not elem.text:
                # Special case: an empty e.g. <events /> container at the root level
                # should be serialized to [], not null
                j[name] = []
            else:
                j[name] = _maybe_intify(elem.text)

    return j