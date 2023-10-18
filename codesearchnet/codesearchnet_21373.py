def main():
    """
        This function obtains hosts from core and starts a nessus scan on these hosts.
        The nessus tag is appended to the host tags.
    """
    config = Config()
    core = HostSearch()
    hosts = core.get_hosts(tags=['!nessus'], up=True)
    hosts = [host for host in hosts]
    host_ips = ",".join([str(host.address) for host in hosts])

    url = config.get('nessus', 'host')
    access = config.get('nessus', 'access_key')
    secret = config.get('nessus', 'secret_key')
    template_name = config.get('nessus', 'template_name')

    nessus = Nessus(access, secret, url, template_name)

    scan_id = nessus.create_scan(host_ips)
    nessus.start_scan(scan_id)

    for host in hosts:
        host.add_tag('nessus')
        host.save()

    Logger().log("nessus", "Nessus scan started on {} hosts".format(len(hosts)), {'scanned_hosts': len(hosts)})