def to_pint(unit):
    """
    Some parsing tweaks to fit pint units / handling of edge cases.
    """
    global HAYSTACK_CONVERSION
    if unit == 'per_minute' or \
        unit == '/min' or \
        unit == 'per_second' or \
        unit == '/s' or \
        unit == 'per_hour' or \
        unit == '/h' or \
        unit == None:
        return ''
        # Those units are not units... they are impossible to fit anywhere in Pint
    for haystack_value, pint_value in HAYSTACK_CONVERSION:
        unit = unit.replace(haystack_value, pint_value)
    return unit