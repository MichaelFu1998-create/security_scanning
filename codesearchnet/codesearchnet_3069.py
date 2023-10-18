def pad(num, n=2, sign=False):
    '''returns n digit string representation of the num'''
    s = unicode(abs(num))
    if len(s) < n:
        s = '0' * (n - len(s)) + s
    if not sign:
        return s
    if num >= 0:
        return '+' + s
    else:
        return '-' + s