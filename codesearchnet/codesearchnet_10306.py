def parse_groups(output):
    """Parse ``make_ndx`` output and return groups as a list of dicts."""
    groups = []
    for line in output.split('\n'):
        m = NDXGROUP.match(line)
        if m:
            d = m.groupdict()
            groups.append({'name': d['GROUPNAME'],
                           'nr': int(d['GROUPNUMBER']),
                           'natoms': int(d['NATOMS'])})
    return groups