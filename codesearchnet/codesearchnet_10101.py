def get_dh_params_length(server_handshake_bytes):
    """
    Determines the length of the DH params from the ServerKeyExchange

    :param server_handshake_bytes:
        A byte string of the handshake data received from the server

    :return:
        None or an integer of the bit size of the DH parameters
    """

    output = None

    dh_params_bytes = None

    for record_type, _, record_data in parse_tls_records(server_handshake_bytes):
        if record_type != b'\x16':
            continue
        for message_type, message_data in parse_handshake_messages(record_data):
            if message_type == b'\x0c':
                dh_params_bytes = message_data
                break
        if dh_params_bytes:
            break

    if dh_params_bytes:
        output = int_from_bytes(dh_params_bytes[0:2]) * 8

    return output