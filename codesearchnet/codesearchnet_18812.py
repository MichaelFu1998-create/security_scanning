def _fields_sort_by_indicators(fields):
    """Sort a set of fields by their indicators.

    Return a sorted list with correct global field positions.
    """
    field_dict = {}
    field_positions_global = []
    for field in fields:
        field_dict.setdefault(field[1:3], []).append(field)
        field_positions_global.append(field[4])

    indicators = field_dict.keys()
    indicators.sort()

    field_list = []
    for indicator in indicators:
        for field in field_dict[indicator]:
            field_list.append(field[:4] + (field_positions_global.pop(0),))

    return field_list