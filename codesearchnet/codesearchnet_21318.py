def nmap_scan():
    """
        Scans the given hosts with nmap.
    """
    # Create the search and config objects
    hs = HostSearch()
    config = Config()

    # Static options to be able to figure out what options to use depending on the input the user gives.
    nmap_types = ['top10', 'top100', 'custom', 'top1000', 'all']
    options = {'top10':'--top-ports 10', 'top100':'--top-ports 100', 'custom': config.get('nmap', 'options'), 'top1000': '--top-ports 1000', 'all': '-p-'}

    # Create an argument parser
    hs_parser = hs.argparser
    argparser = argparse.ArgumentParser(parents=[hs_parser], conflict_handler='resolve', \
    description="Scans hosts from the database using nmap, any arguments that are not in the help are passed to nmap")
    argparser.add_argument('type', metavar='type', \
        help='The number of ports to scan: top10, top100, custom, top1000 (default) or all', \
        type=str, choices=nmap_types, default='top1000', const='top1000', nargs='?')
    arguments, extra_nmap_args = argparser.parse_known_args()

    # Fix the tags for the search
    tags = nmap_types[nmap_types.index(arguments.type):]
    tags = ["!nmap_" + tag  for tag in tags]

    hosts = hs.get_hosts(tags=tags)
    hosts = [host for host in hosts]

    # Create the nmap arguments
    nmap_args = []
    nmap_args.extend(extra_nmap_args)
    nmap_args.extend(options[arguments.type].split(' '))

    # Run nmap
    print_notification("Running nmap with args: {} on {} hosts(s)".format(nmap_args, len(hosts)))
    if len(hosts):
        result = nmap(nmap_args, [str(h.address) for h in hosts])
        # Import the nmap result
        for host in hosts:
            host.add_tag("nmap_{}".format(arguments.type))
            host.save()
        print_notification("Nmap done, importing results")
        stats = import_nmap(result, "nmap_{}".format(arguments.type), check_function=all_hosts, import_services=True)
        stats['scanned_hosts'] = len(hosts)
        stats['type'] = arguments.type

        Logger().log('nmap_scan', "Performed nmap {} scan on {} hosts".format(arguments.type, len(hosts)), stats)
    else:
        print_notification("No hosts found")