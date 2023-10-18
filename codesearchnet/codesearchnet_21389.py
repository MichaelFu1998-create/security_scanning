def get_resolv_dns():
    """
        Returns the dns servers configured in /etc/resolv.conf
    """
    result = []
    try:
        for line in open('/etc/resolv.conf', 'r'):
            if line.startswith('search'):
                result.append(line.strip().split(' ')[1])
    except FileNotFoundError:
        pass
    return result