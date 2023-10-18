def listening_ports():
    """ Reads listening ports from /proc/net/tcp """
    ports = []

    if not os.path.exists(PROC_TCP):
        return ports

    with open(PROC_TCP) as fh:
        for line in fh:
            if '00000000:0000' not in line:
                continue
            parts = line.lstrip(' ').split(' ')
            if parts[2] != '00000000:0000':
                continue

            local_port = parts[1].split(':')[1]
            local_port = int('0x' + local_port, base=16)
            ports.append(local_port)

    return ports