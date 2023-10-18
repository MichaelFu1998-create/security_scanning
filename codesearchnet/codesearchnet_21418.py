def parse_single_computer(entry):
    """
        Parse the entry into a computer object.
    """
    computer = Computer(dns_hostname=get_field(entry, 'dNSHostName'), description=get_field(
        entry, 'description'), os=get_field(entry, 'operatingSystem'), group_id=get_field(entry, 'primaryGroupID'))
    try:
        ip = str(ipaddress.ip_address(get_field(entry, 'IPv4')))
    except ValueError:
        ip = ''

    if ip:
        computer.ip = ip
    elif computer.dns_hostname:
        computer.ip = resolve_ip(computer.dns_hostname)
    return computer