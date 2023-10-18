def get_birthday(code):
    """``get_birthday(code) -> string``

    Birthday of the person whose fiscal code is 'code', in the format DD-MM-YY. 

    Unfortunately it's not possible to guess the four digit birth year, given
    that the Italian fiscal code uses only the last two digits (1983 -> 83).
    Therefore, this function returns a string and not a datetime object.

    eg: birthday('RCCMNL83S18D969H') -> 18-11-83
    """
    assert isvalid(code)

    day = int(code[9:11])
    day = day < 32 and day or day - 40

    month = MONTHSCODE.index(code[8]) + 1
    year = int(code[6:8])

    return "%02d-%02d-%02d" % (day, month, year)