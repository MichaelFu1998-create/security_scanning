def parse(s):
    """
    Parse a string representing a time interval or duration into seconds,
    or raise an exception

    :param str s: a string representation of a time interval
    :raises ValueError: if ``s`` can't be interpreted as a duration

    """

    parts = s.replace(',', ' ').split()
    if not parts:
        raise ValueError('Cannot parse empty string')

    pieces = []
    for part in parts:
        m = PART_MATCH(part)
        pieces.extend(m.groups() if m else [part])

    if len(pieces) == 1:
        pieces.append('s')

    if len(pieces) % 2:
        raise ValueError('Malformed duration %s: %s: %s' % (s, parts, pieces))

    result = 0
    for number, units in zip(*[iter(pieces)] * 2):
        number = float(number)
        if number < 0:
            raise ValueError('Durations cannot have negative components')
        result += number * _get_units(units)

    return result