def numeric(_, n):
    """
    NBASE = 1000
    ndigits = total number of base-NBASE digits
    weight = base-NBASE weight of first digit
    sign = 0x0000 if positive, 0x4000 if negative, 0xC000 if nan
    dscale = decimal digits after decimal place
    """
    try:
        nt = n.as_tuple()
    except AttributeError:
        raise TypeError('numeric field requires Decimal value (got %r)' % n)
    digits = []
    if isinstance(nt.exponent, str):
        # NaN, Inf, -Inf
        ndigits = 0
        weight = 0
        sign = 0xC000
        dscale = 0
    else:
        decdigits = list(reversed(nt.digits + (nt.exponent % 4) * (0,)))
        weight = 0
        while decdigits:
            if any(decdigits[:4]):
                break
            weight += 1
            del decdigits[:4]
        while decdigits:
            digits.insert(0, ndig(decdigits[:4]))
            del decdigits[:4]
        ndigits = len(digits)
        weight += nt.exponent // 4 + ndigits - 1
        sign = nt.sign * 0x4000
        dscale = -min(0, nt.exponent)
    data = [ndigits, weight, sign, dscale] + digits
    return ('ihhHH%dH' % ndigits, [2 * len(data)] + data)