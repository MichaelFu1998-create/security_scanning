def _detect(ip, _isnm):
    """Function internally used to detect the notation of the
    given IP or netmask."""
    ip = str(ip)
    if len(ip) > 1:
        if ip[0:2] == '0x':
            if _CHECK_FUNCT[IP_HEX][_isnm](ip):
                return IP_HEX
        elif ip[0] == '0':
            if _CHECK_FUNCT[IP_OCT][_isnm](ip):
                return IP_OCT
    if _CHECK_FUNCT[IP_DOT][_isnm](ip):
        return IP_DOT
    elif _isnm and _CHECK_FUNCT[NM_BITS][_isnm](ip):
        return NM_BITS
    elif _CHECK_FUNCT[IP_DEC][_isnm](ip):
        return IP_DEC
    elif _isnm and _CHECK_FUNCT[NM_WILDCARD][_isnm](ip):
        return NM_WILDCARD
    elif _CHECK_FUNCT[IP_BIN][_isnm](ip):
        return IP_BIN
    return IP_UNKNOWN