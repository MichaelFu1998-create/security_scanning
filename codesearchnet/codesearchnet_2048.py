def fix(x, digs):
    """Format x as [-]ddd.ddd with 'digs' digits after the point
    and at least one digit before.
    If digs <= 0, the point is suppressed."""
    if type(x) != type(''): x = repr(x)
    try:
        sign, intpart, fraction, expo = extract(x)
    except NotANumber:
        return x
    intpart, fraction = unexpo(intpart, fraction, expo)
    intpart, fraction = roundfrac(intpart, fraction, digs)
    while intpart and intpart[0] == '0': intpart = intpart[1:]
    if intpart == '': intpart = '0'
    if digs > 0: return sign + intpart + '.' + fraction
    else: return sign + intpart