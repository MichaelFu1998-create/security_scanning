def defined_names(request_data):
    """
    Returns the list of defined names for the document.
    """
    global _old_definitions
    ret_val = []
    path = request_data['path']
    toplvl_definitions = jedi.names(
        request_data['code'], path, 'utf-8')
    for d in toplvl_definitions:
        definition = _extract_def(d, path)
        if d.type != 'import':
            ret_val.append(definition)
    ret_val = [d.to_dict() for d in ret_val]
    return ret_val