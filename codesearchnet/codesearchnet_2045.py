def extract(s):
    """Return (sign, intpart, fraction, expo) or raise an exception:
    sign is '+' or '-'
    intpart is 0 or more digits beginning with a nonzero
    fraction is 0 or more digits
    expo is an integer"""
    res = decoder.match(s)
    if res is None: raise NotANumber, s
    sign, intpart, fraction, exppart = res.group(1,2,3,4)
    if sign == '+': sign = ''
    if fraction: fraction = fraction[1:]
    if exppart: expo = int(exppart[1:])
    else: expo = 0
    return sign, intpart, fraction, expo