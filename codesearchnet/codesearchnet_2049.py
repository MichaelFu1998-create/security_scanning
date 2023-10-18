def sci(x, digs):
    """Format x as [-]d.dddE[+-]ddd with 'digs' digits after the point
    and exactly one digit before.
    If digs is <= 0, one digit is kept and the point is suppressed."""
    if type(x) != type(''): x = repr(x)
    sign, intpart, fraction, expo = extract(x)
    if not intpart:
        while fraction and fraction[0] == '0':
            fraction = fraction[1:]
            expo = expo - 1
        if fraction:
            intpart, fraction = fraction[0], fraction[1:]
            expo = expo - 1
        else:
            intpart = '0'
    else:
        expo = expo + len(intpart) - 1
        intpart, fraction = intpart[0], intpart[1:] + fraction
    digs = max(0, digs)
    intpart, fraction = roundfrac(intpart, fraction, digs)
    if len(intpart) > 1:
        intpart, fraction, expo = \
            intpart[0], intpart[1:] + fraction[:-1], \
            expo + len(intpart) - 1
    s = sign + intpart
    if digs > 0: s = s + '.' + fraction
    e = repr(abs(expo))
    e = '0'*(3-len(e)) + e
    if expo < 0: e = '-' + e
    else: e = '+' + e
    return s + 'e' + e