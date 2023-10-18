def import_nmap(result, tag, check_function=all_hosts, import_services=False):
    """
        Imports the given nmap result.
    """
    host_search = HostSearch(arguments=False)
    service_search = ServiceSearch()
    parser = NmapParser()
    report = parser.parse_fromstring(result)
    imported_hosts = 0
    imported_services = 0
    for nmap_host in report.hosts:
        if check_function(nmap_host):
            imported_hosts += 1
            host = host_search.id_to_object(nmap_host.address)
            host.status = nmap_host.status
            host.add_tag(tag)
            if nmap_host.os_fingerprinted:
                host.os = nmap_host.os_fingerprint
            if nmap_host.hostnames:
                host.hostname.extend(nmap_host.hostnames)
            if import_services:
                for service in nmap_host.services:
                    imported_services += 1
                    serv = Service(**service.get_dict())
                    serv.address = nmap_host.address
                    service_id = service_search.object_to_id(serv)
                    if service_id:
                        # Existing object, save the banner and script results.
                        serv_old = Service.get(service_id)
                        if service.banner:
                            serv_old.banner = service.banner
                        # TODO implement
                        # if service.script_results:
                            # serv_old.script_results.extend(service.script_results)
                        serv_old.save()
                    else:
                        # New object
                        serv.address = nmap_host.address
                        serv.save()
                    if service.state == 'open':
                        host.open_ports.append(service.port)
                    if service.state == 'closed':
                        host.closed_ports.append(service.port)
                    if service.state == 'filtered':
                        host.filtered_ports.append(service.port)
            host.save()
    if imported_hosts:
        print_success("Imported {} hosts, with tag {}".format(imported_hosts, tag))
    else:
        print_error("No hosts found")
    return {'hosts': imported_hosts, 'services': imported_services}