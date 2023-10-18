def extract_chain(server_handshake_bytes):
    """
    Extracts the X.509 certificates from the server handshake bytes for use
    when debugging

    :param server_handshake_bytes:
        A byte string of the handshake data received from the server

    :return:
        A list of asn1crypto.x509.Certificate objects
    """

    output = []

    chain_bytes = None

    for record_type, _, record_data in parse_tls_records(server_handshake_bytes):
        if record_type != b'\x16':
            continue
        for message_type, message_data in parse_handshake_messages(record_data):
            if message_type == b'\x0b':
                chain_bytes = message_data
                break
        if chain_bytes:
            break

    if chain_bytes:
        # The first 3 bytes are the cert chain length
        pointer = 3
        while pointer < len(chain_bytes):
            cert_length = int_from_bytes(chain_bytes[pointer:pointer + 3])
            cert_start = pointer + 3
            cert_end = cert_start + cert_length
            pointer = cert_end
            cert_bytes = chain_bytes[cert_start:cert_end]
            output.append(Certificate.load(cert_bytes))

    return output