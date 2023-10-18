def normalize_housecode(house_code):
    """Returns a normalized house code, i.e. upper case.
    Raises exception X10InvalidHouseCode if house code appears to be invalid
    """
    if house_code is None:
        raise X10InvalidHouseCode('%r is not a valid house code' % house_code)
    if not isinstance(house_code, basestring):
        raise X10InvalidHouseCode('%r is not a valid house code' % house_code)
    if len(house_code) != 1:
        raise X10InvalidHouseCode('%r is not a valid house code' % house_code)
    house_code = house_code.upper()
    if not ('A' <= house_code <= 'P'):
        raise X10InvalidHouseCode('%r is not a valid house code' % house_code)
    return house_code