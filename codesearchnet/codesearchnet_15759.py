def bik():
    """Return a random bank identification number."""
    return '04' + \
           ''.join([str(random.randint(1, 9)) for _ in range(5)]) + \
           str(random.randint(0, 49) + 50)