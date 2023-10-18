def convert(ip, notation=IP_DOT, inotation=IP_UNKNOWN, check=True):
    """Convert among IP address notations.

    Given an IP address, this function returns the address
    in another notation.

    @param ip: the IP address.
    @type ip: integers, strings or object with an appropriate __str()__ method.

    @param notation: the notation of the output (default: IP_DOT).
    @type notation: one of the IP_* constants, or the equivalent strings.

    @param inotation: force the input to be considered in the given notation
                    (default the notation of the input is autodetected).
    @type inotation: one of the IP_* constants, or the equivalent strings.

    @param check: force the notation check on the input.
    @type check: True force the check, False force not to check and None
                do the check only if the inotation is unknown.

    @return: a string representing the IP in the selected notation.

    @raise ValueError: raised when the input is in unknown notation."""
    return _convert(ip, notation, inotation, _check=check, _isnm=False)