def street_number():
    """Return a random street number."""
    length = int(random.choice(string.digits[1:6]))
    return ''.join(random.sample(string.digits, length))