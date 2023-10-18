def generate(length=DEFAULT_LENGTH):
    """
    Generate a random string of the specified length.

    The returned string is composed of an alphabet that shouldn't include any
    characters that are easily mistakeable for one another (I, 1, O, 0), and
    hopefully won't accidentally contain any English-language curse words.
    """
    return ''.join(random.SystemRandom().choice(ALPHABET)
                   for _ in range(length))