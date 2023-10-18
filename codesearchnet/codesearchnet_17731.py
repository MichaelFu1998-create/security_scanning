def normalize_unitnumber(unit_number):
    """Returns a normalized unit number, i.e. integers
    Raises exception X10InvalidUnitNumber if unit number appears to be invalid
    """
    try:
        try:
            unit_number = int(unit_number)
        except ValueError:
            raise X10InvalidUnitNumber('%r not a valid unit number' % unit_number)
    except TypeError:
        raise X10InvalidUnitNumber('%r not a valid unit number' % unit_number)
    if not (1 <= unit_number <= 16):
        raise X10InvalidUnitNumber('%r not a valid unit number' % unit_number)
    return unit_number