def parse_domain_computers(filename):
    """
        Parse the file and extract the computers, import the computers that resolve into jackal.
    """
    with open(filename) as f:
        data = json.loads(f.read())
    hs = HostSearch()
    count = 0
    entry_count = 0
    print_notification("Parsing {} entries".format(len(data)))
    for system in data:
        entry_count += 1
        parsed = parse_single_computer(system)
        if parsed.ip:
            try:
                host = hs.id_to_object(parsed.ip)
                host.description.append(parsed.description)
                host.hostname.append(parsed.dns_hostname)
                if parsed.os:
                    host.os = parsed.os
                host.domain_controller = parsed.dc
                host.add_tag('domaindump')
                host.save()
                count += 1
            except ValueError:
                pass
        sys.stdout.write('\r')
        sys.stdout.write(
            "[{}/{}] {} resolved".format(entry_count, len(data), count))
        sys.stdout.flush()
    sys.stdout.write('\r')
    return count