def itruediv(a, b):
    "Same as a /= b."
    if type(a) == int or type(a) == long:
        a = float(a)
    a /= b
    return a