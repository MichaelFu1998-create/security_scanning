def get_hosts_for_site(site=None):
    """
    Returns a list of hosts that have been configured to support the given site.
    """
    site = site or env.SITE
    hosts = set()
    for hostname, _sites in six.iteritems(env.available_sites_by_host):
#         print('checking hostname:',hostname, _sites)
        for _site in _sites:
            if _site == site:
#                 print( '_site:',_site)
                host_ip = get_host_ip(hostname)
#                 print( 'host_ip:',host_ip)
                if host_ip:
                    hosts.add(host_ip)
                    break
    return list(hosts)