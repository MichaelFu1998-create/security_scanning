def legal_inn():
    """Return a random taxation ID number for a company."""
    mask = [2, 4, 10, 3, 5, 9, 4, 6, 8]
    inn = [random.randint(1, 9) for _ in range(10)]
    weighted = [v * mask[i] for i, v in enumerate(inn[:-1])]
    inn[9] = sum(weighted) % 11 % 10
    return "".join(map(str, inn))