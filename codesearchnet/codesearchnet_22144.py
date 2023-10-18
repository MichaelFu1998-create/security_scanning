def is_colour(value):
    """Returns True if the value given is a valid CSS colour, i.e. matches one
    of the regular expressions in the module or is in the list of
    predetefined values by the browser.
    """
    global PREDEFINED, HEX_MATCH, RGB_MATCH, RGBA_MATCH, HSL_MATCH, HSLA_MATCH
    value = value.strip()

    # hex match
    if HEX_MATCH.match(value) or RGB_MATCH.match(value) or \
            RGBA_MATCH.match(value) or HSL_MATCH.match(value) or \
            HSLA_MATCH.match(value) or value in PREDEFINED:
        return True

    return False