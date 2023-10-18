def parse_session_info(server_handshake_bytes, client_handshake_bytes):
    """
    Parse the TLS handshake from the client to the server to extract information
    including the cipher suite selected, if compression is enabled, the
    session id and if a new or reused session ticket exists.

    :param server_handshake_bytes:
        A byte string of the handshake data received from the server

    :param client_handshake_bytes:
        A byte string of the handshake data sent to the server

    :return:
        A dict with the following keys:
         - "protocol": unicode string
         - "cipher_suite": unicode string
         - "compression": boolean
         - "session_id": "new", "reused" or None
         - "session_ticket: "new", "reused" or None
    """

    protocol = None
    cipher_suite = None
    compression = False
    session_id = None
    session_ticket = None

    server_session_id = None
    client_session_id = None

    for record_type, _, record_data in parse_tls_records(server_handshake_bytes):
        if record_type != b'\x16':
            continue
        for message_type, message_data in parse_handshake_messages(record_data):
            # Ensure we are working with a ServerHello message
            if message_type != b'\x02':
                continue
            protocol = {
                b'\x03\x00': "SSLv3",
                b'\x03\x01': "TLSv1",
                b'\x03\x02': "TLSv1.1",
                b'\x03\x03': "TLSv1.2",
                b'\x03\x04': "TLSv1.3",
            }[message_data[0:2]]

            session_id_length = int_from_bytes(message_data[34:35])
            if session_id_length > 0:
                server_session_id = message_data[35:35 + session_id_length]

            cipher_suite_start = 35 + session_id_length
            cipher_suite_bytes = message_data[cipher_suite_start:cipher_suite_start + 2]
            cipher_suite = CIPHER_SUITE_MAP[cipher_suite_bytes]

            compression_start = cipher_suite_start + 2
            compression = message_data[compression_start:compression_start + 1] != b'\x00'

            extensions_length_start = compression_start + 1
            extensions_data = message_data[extensions_length_start:]
            for extension_type, extension_data in _parse_hello_extensions(extensions_data):
                if extension_type == 35:
                    session_ticket = "new"
                    break
            break

    for record_type, _, record_data in parse_tls_records(client_handshake_bytes):
        if record_type != b'\x16':
            continue
        for message_type, message_data in parse_handshake_messages(record_data):
            # Ensure we are working with a ClientHello message
            if message_type != b'\x01':
                continue

            session_id_length = int_from_bytes(message_data[34:35])
            if session_id_length > 0:
                client_session_id = message_data[35:35 + session_id_length]

            cipher_suite_start = 35 + session_id_length
            cipher_suite_length = int_from_bytes(message_data[cipher_suite_start:cipher_suite_start + 2])

            compression_start = cipher_suite_start + 2 + cipher_suite_length
            compression_length = int_from_bytes(message_data[compression_start:compression_start + 1])

            # On subsequent requests, the session ticket will only be seen
            # in the ClientHello message
            if server_session_id is None and session_ticket is None:
                extensions_length_start = compression_start + 1 + compression_length
                extensions_data = message_data[extensions_length_start:]
                for extension_type, extension_data in _parse_hello_extensions(extensions_data):
                    if extension_type == 35:
                        session_ticket = "reused"
                        break
            break

    if server_session_id is not None:
        if client_session_id is None:
            session_id = "new"
        else:
            if client_session_id != server_session_id:
                session_id = "new"
            else:
                session_id = "reused"

    return {
        "protocol": protocol,
        "cipher_suite": cipher_suite,
        "compression": compression,
        "session_id": session_id,
        "session_ticket": session_ticket,
    }