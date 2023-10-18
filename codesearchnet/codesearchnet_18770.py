def create_field(subfields=None, ind1=' ', ind2=' ', controlfield_value='',
                 global_position=-1):
    """
    Return a field created with the provided elements.

    Global position is set arbitrary to -1.
    """
    if subfields is None:
        subfields = []

    ind1, ind2 = _wash_indicators(ind1, ind2)
    field = (subfields, ind1, ind2, controlfield_value, global_position)
    _check_field_validity(field)
    return field