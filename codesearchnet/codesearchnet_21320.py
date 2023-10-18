def os_discovery():
    """
        Performs os (and domain) discovery of smb hosts.
    """
    hs = HostSearch()

    hosts = hs.get_hosts(ports=[445], tags=['!nmap_os'])

    # TODO fix filter for emtpy fields.
    hosts = [host for host in hosts if not host.os]

    host_dict = {}
    for host in hosts:
        host_dict[str(host.address)] = host

    arguments = "--script smb-os-discovery.nse -p 445 -Pn -n --disable-arp-ping".split(' ')
    if len(hosts):
        count = 0
        print_notification("Checking OS of {} systems".format(len(hosts)))
        result = nmap(arguments, [str(h.address) for h in hosts])

        parser = NmapParser()
        report = parser.parse_fromstring(result)

        for nmap_host in report.hosts:
            for script_result in nmap_host.scripts_results:
                script_result = script_result.get('elements', {})

                host = host_dict[str(nmap_host.address)]
                if 'fqdn' in script_result:
                    host.hostname.append(script_result['fqdn'])
                if 'os' in script_result:
                    count += 1
                    host.os = script_result['os']

                host_dict[str(nmap_host.address)] = host

        for host in hosts:
            host.add_tag('nmap_os')
            host.save()

        print_notification("Done, found the os of {} systems".format(count))

    else:
        print_notification("No systems found to be checked.")