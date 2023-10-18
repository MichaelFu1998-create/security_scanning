def detect_other_protocol(server_handshake_bytes):
    """
    Looks at the server handshake bytes to try and detect a different protocol

    :param server_handshake_bytes:
        A byte string of the handshake data received from the server

    :return:
        None, or a unicode string of "ftp", "http", "imap", "pop3", "smtp"
    """

    if server_handshake_bytes[0:5] == b'HTTP/':
        return 'HTTP'

    if server_handshake_bytes[0:4] == b'220 ':
        if re.match(b'^[^\r\n]*ftp', server_handshake_bytes, re.I):
            return 'FTP'
        else:
            return 'SMTP'

    if server_handshake_bytes[0:4] == b'220-':
        return 'FTP'

    if server_handshake_bytes[0:4] == b'+OK ':
        return 'POP3'

    if server_handshake_bytes[0:4] == b'* OK' or server_handshake_bytes[0:9] == b'* PREAUTH':
        return 'IMAP'

    return None