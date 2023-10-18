def sentences(quantity=2, as_list=False):
    """Return random sentences."""
    result = [sntc.strip() for sntc in
              random.sample(get_dictionary('lorem_ipsum'), quantity)]

    if as_list:
        return result
    else:
        return ' '.join(result)