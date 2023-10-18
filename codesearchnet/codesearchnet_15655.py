def passcode(callsign):
    """
    Takes a CALLSIGN and returns passcode
    """
    assert isinstance(callsign, str)

    callsign = callsign.split('-')[0].upper()

    code = 0x73e2
    for i, char in enumerate(callsign):
        code ^= ord(char) << (8 if not i % 2 else 0)

    return code & 0x7fff