def characters(quantity=10):
    """Return random characters."""
    line = map(_to_lower_alpha_only,
               ''.join(random.sample(get_dictionary('lorem_ipsum'), quantity)))
    return ''.join(line)[:quantity]