def check_hex(value):
    """
    Check if the given hex value is a valid RGB color

    It should match the format: [0-9a-fA-F]
    and be of length 3 or 6.
    """
    length = len(value)
    if length not in (3, 6):
        raise ValueError('Hex string #{} is too long'.format(value))

    regex = r'[0-9a-f]{{{length}}}'.format(length=length)
    if not re.search(regex, value, re.I):
        raise ValueError('Invalid Hex String: #{}'.format(value))