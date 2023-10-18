def parse_alert(server_handshake_bytes):
    """
    Parses the handshake for protocol alerts

    :param server_handshake_bytes:
        A byte string of the handshake data received from the server

    :return:
        None or an 2-element tuple of integers:
         0: 1 (warning) or 2 (fatal)
         1: The alert description (see https://tools.ietf.org/html/rfc5246#section-7.2)
    """

    for record_type, _, record_data in parse_tls_records(server_handshake_bytes):
        if record_type != b'\x15':
            continue
        if len(record_data) != 2:
            return None
        return (int_from_bytes(record_data[0:1]), int_from_bytes(record_data[1:2]))
    return None