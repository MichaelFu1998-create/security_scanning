def _convert(ip, notation, inotation, _check, _isnm):
    """Internally used to convert IPs and netmasks to other notations."""
    inotation_orig = inotation
    notation_orig = notation
    inotation = _get_notation(inotation)
    notation = _get_notation(notation)
    if inotation is None:
        raise ValueError('_convert: unknown input notation: "%s"' % inotation_orig)
    if notation is None:
        raise ValueError('_convert: unknown output notation: "%s"' % notation_orig)
    docheck = _check or False
    if inotation == IP_UNKNOWN:
        inotation = _detect(ip, _isnm)
        if inotation == IP_UNKNOWN:
            raise ValueError('_convert: unable to guess input notation or invalid value')
        if _check is None:
            docheck = True
    # We _always_ check this case later.
    if _isnm:
        docheck = False
    dec = 0
    if inotation == IP_DOT:
        dec = _dot_to_dec(ip, docheck)
    elif inotation == IP_HEX:
        dec = _hex_to_dec(ip, docheck)
    elif inotation == IP_BIN:
        dec = _bin_to_dec(ip, docheck)
    elif inotation == IP_OCT:
        dec = _oct_to_dec(ip, docheck)
    elif inotation == IP_DEC:
        dec = _dec_to_dec_long(ip, docheck)
    elif _isnm and inotation == NM_BITS:
        dec = _bits_to_dec(ip, docheck)
    elif _isnm and inotation == NM_WILDCARD:
        dec = _wildcard_to_dec(ip, docheck)
    else:
        raise ValueError('_convert: unknown IP/netmask notation: "%s"' % inotation_orig)
    # Ensure this is a valid netmask.
    if _isnm and dec not in _NETMASKS_VALUES:
        raise ValueError('_convert: invalid netmask: "%s"' % ip)
    if notation == IP_DOT:
        return _dec_to_dot(dec)
    elif notation == IP_HEX:
        return _dec_to_hex(dec)
    elif notation == IP_BIN:
        return _dec_to_bin(dec)
    elif notation == IP_OCT:
        return _dec_to_oct(dec)
    elif notation == IP_DEC:
        return _dec_to_dec_str(dec)
    elif _isnm and notation == NM_BITS:
        return _dec_to_bits(dec)
    elif _isnm and notation == NM_WILDCARD:
        return _dec_to_wildcard(dec)
    else:
        raise ValueError('convert: unknown notation: "%s"' % notation_orig)