def with_unit(number, unit=None):
    """ Return number with unit
    args:
        number (mixed): Number
        unit (str): Unit
    returns:
        str
    """
    if isinstance(number, tuple):
        number, unit = number
    if number == 0:
        return '0'
    if unit:
        number = str(number)
        if number.startswith('.'):
            number = '0' + number
        return "%s%s" % (number, unit)
    return number if isinstance(number, string_types) else str(number)