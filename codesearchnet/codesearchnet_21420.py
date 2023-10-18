def parse_user(entry, domain_groups):
    """
        Parses a single entry from the domaindump
    """
    result = {}
    distinguished_name = get_field(entry, 'distinguishedName')
    result['domain'] = ".".join(distinguished_name.split(',DC=')[1:])
    result['name'] = get_field(entry, 'name')
    result['username'] = get_field(entry, 'sAMAccountName')
    result['description'] = get_field(entry, 'description')
    result['sid'] = get_field(entry, 'objectSid').split('-')[-1]

    primary_group = get_field(entry, 'primaryGroupID')
    member_of = entry['attributes'].get('memberOf', [])
    groups = []
    for member in member_of:
        for e in member.split(','):
            if e.startswith('CN='):
                groups.append(e[3:])
    groups.append(domain_groups.get(primary_group, ''))
    result['groups'] = groups

    flags = []
    try:
        uac = int(get_field(entry, 'userAccountControl'))

        for flag, value in uac_flags.items():
            if uac & value:
                flags.append(flag)
    except ValueError:
        pass
    result['flags'] = flags
    return result