def _is_prime(bit_size, n):
    """
    An implementation of Miller–Rabin for checking if a number is prime.

    :param bit_size:
        An integer of the number of bits in the prime number

    :param n:
        An integer, the prime number

    :return:
        A boolean
    """

    r = 0
    s = n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    if bit_size >= 1300:
        k = 2
    elif bit_size >= 850:
        k = 3
    elif bit_size >= 650:
        k = 4
    elif bit_size >= 550:
        k = 5
    elif bit_size >= 450:
        k = 6

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True