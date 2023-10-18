def parse_domain_users(domain_users_file, domain_groups_file):
    """
        Parses the domain users and groups files.
    """
    with open(domain_users_file) as f:
        users = json.loads(f.read())

    domain_groups = {}
    if domain_groups_file:
        with open(domain_groups_file) as f:
            groups = json.loads(f.read())
            for group in groups:
                sid = get_field(group, 'objectSid')
                domain_groups[int(sid.split('-')[-1])] = get_field(group, 'cn')

    user_search = UserSearch()
    count = 0
    total = len(users)
    print_notification("Importing {} users".format(total))
    for entry in users:
        result = parse_user(entry, domain_groups)
        user = user_search.id_to_object(result['username'])
        user.name = result['name']
        user.domain.append(result['domain'])
        user.description = result['description']
        user.groups.extend(result['groups'])
        user.flags.extend(result['flags'])
        user.sid = result['sid']
        user.add_tag("domaindump")
        user.save()
        count += 1
        sys.stdout.write('\r')
        sys.stdout.write("[{}/{}]".format(count, total))
        sys.stdout.flush()
    sys.stdout.write('\r')
    return count