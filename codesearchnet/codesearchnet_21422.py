def import_domaindump():
    """
        Parses ldapdomaindump files and stores hosts and users in elasticsearch.
    """
    parser = argparse.ArgumentParser(
        description="Imports users, groups and computers result files from the ldapdomaindump tool, will resolve the names from domain_computers output for IPs")
    parser.add_argument("files", nargs='+',
                        help="The domaindump files to import")
    arguments = parser.parse_args()
    domain_users_file = ''
    domain_groups_file = ''
    computer_count = 0
    user_count = 0
    stats = {}
    for filename in arguments.files:
        if filename.endswith('domain_computers.json'):
            print_notification('Parsing domain computers')
            computer_count = parse_domain_computers(filename)
            if computer_count:
                stats['hosts'] = computer_count
                print_success("{} hosts imported".format(computer_count))
        elif filename.endswith('domain_users.json'):
            domain_users_file = filename
        elif filename.endswith('domain_groups.json'):
            domain_groups_file = filename
    if domain_users_file:
        print_notification("Parsing domain users")
        user_count = parse_domain_users(domain_users_file, domain_groups_file)
        if user_count:
            print_success("{} users imported".format(user_count))
            stats['users'] = user_count
    Logger().log("import_domaindump", 'Imported domaindump, found {} user, {} systems'.format(user_count, computer_count), stats)