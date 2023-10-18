def truediv(a, b):
    "Same as a / b."
    if type(a) == int or type(a) == long:
        a = float(a)
    return a / b