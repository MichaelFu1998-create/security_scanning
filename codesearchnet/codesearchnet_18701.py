def add_nations_field(authors_subfields):
    """Add correct nations field according to mapping in NATIONS_DEFAULT_MAP."""
    from .config import NATIONS_DEFAULT_MAP
    result = []
    for field in authors_subfields:
        if field[0] == 'v':
            values = [x.replace('.', '') for x in field[1].split(', ')]
            possible_affs = filter(lambda x: x is not None,
                                   map(NATIONS_DEFAULT_MAP.get, values))
            if 'CERN' in possible_affs and 'Switzerland' in possible_affs:
                # Don't use remove in case of multiple Switzerlands
                possible_affs = [x for x in possible_affs
                                 if x != 'Switzerland']

            result.extend(possible_affs)

    result = sorted(list(set(result)))

    if result:
        authors_subfields.extend([('w', res) for res in result])
    else:
        authors_subfields.append(('w', 'HUMAN CHECK'))