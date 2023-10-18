def legal_ogrn():
    """Return a random government registration ID for a company."""
    ogrn = "".join(map(str, [random.randint(1, 9) for _ in range(12)]))
    ogrn += str((int(ogrn) % 11 % 10))
    return ogrn