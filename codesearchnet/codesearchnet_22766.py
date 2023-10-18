def parse_hub_key(key):
    """Parse a hub key into a dictionary of component parts

    :param key: str, a hub key
    :returns: dict, hub key split into parts
    :raises: ValueError
    """
    if key is None:
        raise ValueError('Not a valid key')

    match = re.match(PATTERN, key)
    if not match:
        match = re.match(PATTERN_S0, key)
        if not match:
            raise ValueError('Not a valid key')

        return dict(map(normalise_part, zip([p for p in PARTS_S0.keys()], match.groups())))

    return dict(zip(PARTS.keys(), match.groups()))