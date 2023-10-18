def nmap_discover():
    """
        This function retrieves ranges from jackal
        Uses two functions of nmap to find hosts:
            ping:   icmp / arp pinging of targets
            lookup: reverse dns lookup
    """
    rs = RangeSearch()
    rs_parser = rs.argparser
    arg = argparse.ArgumentParser(parents=[rs_parser], conflict_handler='resolve')
    arg.add_argument('type', metavar='type', \
        help='The type of nmap scan to do, choose from ping or lookup', \
        type=str, choices=['ping', 'lookup'])
    arguments, nmap_args = arg.parse_known_args()

    tag = None
    if arguments.type == 'ping':
        tag = 'nmap_ping'
        nmap_args.append('-sn')
        nmap_args.append('-n')
        check_function = include_up_hosts
    elif arguments.type == 'lookup':
        tag = 'nmap_lookup'
        nmap_args.append('-sL')
        check_function = include_hostnames

    ranges = rs.get_ranges(tags=['!{}'.format(tag)])
    ranges = [r for r in ranges]
    ips = []
    for r in ranges:
        ips.append(r.range)

    print_notification("Running nmap with args: {} on {} range(s)".format(nmap_args, len(ips)))
    result = nmap(nmap_args, ips)
    stats = import_nmap(result, tag, check_function)
    stats['scanned_ranges'] = len(ips)

    Logger().log('nmap_discover', "Nmap discover with args: {} on {} range(s)".format(nmap_args, len(ips)), stats)

    for r in ranges:
        r.add_tag(tag)
        r.save()