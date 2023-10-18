def to_haystack(unit):
    """
    Some parsing tweaks to fit pint units / handling of edge cases.
    """
    unit = str(unit)
    global HAYSTACK_CONVERSION
    global PINT_CONVERSION
    if unit == 'per_minute' or \
        unit == '/min' or \
        unit == 'per_second' or \
        unit == '/s' or \
        unit == 'per_hour' or \
        unit == '/h' or \
        unit == None:
        return ''
        # Those units are not units... they are impossible to fit anywhere in Pint
    
    for pint_value, haystack_value in PINT_CONVERSION:
        unit = unit.replace(pint_value, haystack_value)
    for haystack_value, pint_value in HAYSTACK_CONVERSION:
        if pint_value == '':
            continue
        unit = unit.replace(pint_value, haystack_value)
    return unit