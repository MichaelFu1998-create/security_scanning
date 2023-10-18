def nmap_smb_vulnscan():
    """
        Scans available smb services in the database for smb signing and ms17-010.
    """
    service_search = ServiceSearch()
    services = service_search.get_services(ports=['445'], tags=['!smb_vulnscan'], up=True)
    services = [service for service in services]
    service_dict = {}
    for service in services:
        service.add_tag('smb_vulnscan')
        service_dict[str(service.address)] = service

    nmap_args = "-Pn -n --disable-arp-ping --script smb-security-mode.nse,smb-vuln-ms17-010.nse -p 445".split(" ")

    if services:
        result = nmap(nmap_args, [str(s.address) for s in services])
        parser = NmapParser()
        report = parser.parse_fromstring(result)
        smb_signing = 0
        ms17 = 0
        for nmap_host in report.hosts:
            for script_result in nmap_host.scripts_results:
                script_result = script_result.get('elements', {})
                service = service_dict[str(nmap_host.address)]
                if script_result.get('message_signing', '') == 'disabled':
                    print_success("({}) SMB Signing disabled".format(nmap_host.address))
                    service.add_tag('smb_signing_disabled')
                    smb_signing += 1
                if script_result.get('CVE-2017-0143', {}).get('state', '') == 'VULNERABLE':
                    print_success("({}) Vulnerable for MS17-010".format(nmap_host.address))
                    service.add_tag('MS17-010')
                    ms17 += 1
                service.update(tags=service.tags)

        print_notification("Completed, 'smb_signing_disabled' tag added to systems with smb signing disabled, 'MS17-010' tag added to systems that did not apply MS17-010.")
        stats = {'smb_signing': smb_signing, 'MS17_010': ms17, 'scanned_services': len(services)}

        Logger().log('smb_vulnscan', 'Scanned {} smb services for vulnerabilities'.format(len(services)), stats)
    else:
        print_notification("No services found to scan.")