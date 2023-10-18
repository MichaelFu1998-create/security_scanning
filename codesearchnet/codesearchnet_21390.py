def zone_transfer(address, dns_name):
    """
        Tries to perform a zone transfer.
    """
    ips = []
    try:
        print_notification("Attempting dns zone transfer for {} on {}".format(dns_name, address))
        z = dns.zone.from_xfr(dns.query.xfr(address, dns_name))
    except dns.exception.FormError:
        print_notification("Zone transfer not allowed")
        return ips
    names = z.nodes.keys()
    print_success("Zone transfer successfull for {}, found {} entries".format(address, len(names)))
    for n in names:
        node = z[n]
        data = node.get_rdataset(dns.rdataclass.IN, dns.rdatatype.A)
        if data:
            # TODO add hostnames to entries.
            # hostname = n.to_text()
            for item in data.items:
                address = item.address
                ips.append(address)
    return ips