def resolve_domains(domains, disable_zone=False):
    """
        Resolves the list of domains and returns the ips.
    """
    dnsresolver = dns.resolver.Resolver()

    ips = []

    for domain in domains:
        print_notification("Resolving {}".format(domain))
        try:
            result = dnsresolver.query(domain, 'A')
            for a in result.response.answer[0]:
                ips.append(str(a))
                if not disable_zone:
                    ips.extend(zone_transfer(str(a), domain))
        except dns.resolver.NXDOMAIN as e:
            print_error(e)
    return ips