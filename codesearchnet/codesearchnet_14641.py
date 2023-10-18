def generate_passphrase(size=12):
    """Return a generate string `size` long based on lowercase, uppercase,
    and digit chars
    """
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return str(''.join(random.choice(chars) for _ in range(size)))