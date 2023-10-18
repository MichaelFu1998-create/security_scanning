def phone():
    """Return a random phone number in `#-(###)###-####` format."""
    format = '#-(###)###-####'

    result = ''
    for item in format:
        if item == '#':
            result += str(random.randint(0, 9))
        else:
            result += item

    return result