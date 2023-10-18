def parse_ips(ips, netmask, include_public):
    """
        Parses the list of ips, turns these into ranges based on the netmask given.
        Set include_public to True to include public IP adresses.
    """
    hs = HostSearch()
    rs = RangeSearch()
    ranges = []
    ips = list(set(ips))
    included_ips = []
    print_success("Found {} ips".format(len(ips)))
    for ip in ips:
        ip_address = ipaddress.ip_address(ip)
        if include_public or ip_address.is_private:
            # To stop the screen filling with ranges.
            if len(ips) < 15:
                print_success("Found ip: {}".format(ip))
            host = hs.id_to_object(ip)
            host.add_tag('dns_discover')
            host.save()
            r = str(ipaddress.IPv4Network("{}/{}".format(ip, netmask), strict=False))
            ranges.append(r)
            included_ips.append(ip)
        else:
            print_notification("Excluding ip {}".format(ip))

    ranges = list(set(ranges))
    print_success("Found {} ranges".format(len(ranges)))
    for rng in ranges:
        # To stop the screen filling with ranges.
        if len(ranges) < 15:
            print_success("Found range: {}".format(rng))
        r = rs.id_to_object(rng)
        r.add_tag('dns_discover')
        r.save()

    stats = {}
    stats['ips'] = included_ips
    stats['ranges'] = ranges
    return stats