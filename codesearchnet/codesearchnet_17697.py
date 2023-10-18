def offset_random_rgb(seed, amount=1):
    """
    Given a seed color, generate a specified number of random colors (1 color by default) determined by a randomized
    offset from the seed.

    :param seed:
    :param amount:
    :return:
    """
    r, g, b = seed

    results = []
    for _ in range(amount):
        base_val = ((r + g + b) / 3) + 1  # Add one to eliminate case where the base value would otherwise be 0
        new_val = base_val + (random.random() * rgb_max_val / 5)  # Randomly offset with an arbitrary multiplier
        ratio = new_val / base_val
        results.append((min(int(r*ratio), rgb_max_val), min(int(g*ratio), rgb_max_val), min(int(b*ratio), rgb_max_val)))

    return results[0] if len(results) > 1 else results