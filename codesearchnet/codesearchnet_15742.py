def zip_code():
    """Return a random ZIP code, either in `#####` or `#####-####` format."""
    format = '#####'
    if random.random() >= 0.5:
        format = '#####-####'

    result = ''
    for item in format:
        if item == '#':
            result += str(random.randint(0, 9))
        else:
            result += item

    return result