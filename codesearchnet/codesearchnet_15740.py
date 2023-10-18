def number(type=None, length=None, prefixes=None):
    """
    Return a random credit card number.

    :param type: credit card type. Defaults to a random selection.
    :param length: length of the credit card number.
                   Defaults to the length for the selected card type.
    :param prefixes: allowed prefixes for the card number.
                     Defaults to prefixes for the selected card type.
    :return: credit card randomly generated number (int)
    """
    # select credit card type
    if type and type in CARDS:
        card = type
    else:
        card = random.choice(list(CARDS.keys()))

    # select a credit card number's prefix
    if not prefixes:
        prefixes = CARDS[card]['prefixes']
    prefix = random.choice(prefixes)

    # select length of the credit card number, if it's not set
    if not length:
        length = CARDS[card]['length']

    # generate all digits but the last one
    result = str(prefix)

    for d in range(length - len(str(prefix))):
        result += str(basic.number())

    last_digit = check_digit(int(result))

    return int(result[:-1] + str(last_digit))