def person_inn():
    """Return a random taxation ID number for a natural person."""
    mask11 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
    mask12 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
    inn = [random.randint(1, 9) for _ in range(12)]

    # get the 11th digit of the INN
    weighted11 = [v * mask11[i] for i, v in enumerate(inn[:-2])]
    inn[10] = sum(weighted11) % 11 % 10

    # get the 12th digit of the INN
    weighted12 = [v * mask12[i] for i, v in enumerate(inn[:-1])]
    inn[11] = sum(weighted12) % 11 % 10

    return "".join(map(str, inn))