def fill_gaps(list_dicts):
    """
    Fill gaps in a list of dictionaries. Add empty keys to dictionaries in
    the list that don't contain other entries' keys

    :param list_dicts: A list of dictionaries
    :return: A list of field names, a list of dictionaries with identical keys
    """

    field_names = []  # != set bc. preserving order is better for output
    for datum in list_dicts:
        for key in datum.keys():
            if key not in field_names:
                field_names.append(key)
    for datum in list_dicts:
        for key in field_names:
            if key not in datum:
                datum[key] = ''
    return list(field_names), list_dicts