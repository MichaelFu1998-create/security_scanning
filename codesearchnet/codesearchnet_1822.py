def indexOf(a, b):
    "Return the first index of b in a."
    for i, j in enumerate(a):
        if j == b:
            return i
    else:
        raise ValueError('sequence.index(x): x not in sequence')