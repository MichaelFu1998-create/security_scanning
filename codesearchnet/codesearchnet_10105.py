def parse_handshake_messages(data):
    """
    Creates a generator returning tuples of information about each message in
    a byte string of data from a TLS handshake record

    :param data:
        A byte string of a TLS handshake record data

    :return:
        A generator that yields 2-element tuples:
        [0] Byte string of message type
        [1] Byte string of message data
    """

    pointer = 0
    data_len = len(data)
    while pointer < data_len:
        length = int_from_bytes(data[pointer + 1:pointer + 4])
        yield (
            data[pointer:pointer + 1],
            data[pointer + 4:pointer + 4 + length]
        )
        pointer += 4 + length