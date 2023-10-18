def _ip_for_mac_from_ip_addr_show(ip_addr_show, target_mac):
    """Given the rather-complex output from an 'ip addr show' command
    on the VM, parse the output to determine the IP address
    assigned to the interface with the given MAC."""
    return_next_ip = False
    for line in ip_addr_show.splitlines():
        line = line.strip()
        if line.startswith('link/ether'):
            line_mac = line.split(' ')[1].replace(':', '')
            if line_mac == target_mac:
                return_next_ip = True
        elif return_next_ip and line.startswith('inet') and not line.startswith('inet6'):
            ip = line.split(' ')[1].split('/')[0]
            return ip