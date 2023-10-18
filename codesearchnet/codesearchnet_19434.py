def exact_sqrt(n2):
    "If n2 is a perfect square, return its square root, else raise error."
    n = int(math.sqrt(n2))
    assert n * n == n2
    return n