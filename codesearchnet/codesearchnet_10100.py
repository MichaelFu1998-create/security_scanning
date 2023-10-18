def detect_client_auth_request(server_handshake_bytes):
    """
    Determines if a CertificateRequest message is sent from the server asking
    the client for a certificate

    :param server_handshake_bytes:
        A byte string of the handshake data received from the server

    :return:
        A boolean - if a client certificate request was found
    """

    for record_type, _, record_data in parse_tls_records(server_handshake_bytes):
        if record_type != b'\x16':
            continue
        for message_type, message_data in parse_handshake_messages(record_data):
            if message_type == b'\x0d':
                return True
    return False