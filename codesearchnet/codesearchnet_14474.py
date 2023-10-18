def get_ip_packet(data, client_port, server_port, is_loopback=False):
    """ if client_port is 0 any client_port is good """
    header = _loopback if is_loopback else _ethernet

    try:
        header.unpack(data)
    except Exception as ex:
        raise ValueError('Bad header: %s' % ex)

    tcp_p = getattr(header.data, 'data', None)
    if type(tcp_p) != dpkt.tcp.TCP:
        raise ValueError('Not a TCP packet')

    if tcp_p.dport == server_port:
        if client_port != 0 and tcp_p.sport != client_port:
            raise ValueError('Request from different client')
    elif tcp_p.sport == server_port:
        if client_port != 0 and tcp_p.dport != client_port:
            raise ValueError('Reply for different client')
    else:
        raise ValueError('Packet not for/from client/server')

    return header.data