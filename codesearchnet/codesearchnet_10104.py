def parse_tls_records(data):
    """
    Creates a generator returning tuples of information about each record
    in a byte string of data from a TLS client or server. Stops as soon as it
    find a ChangeCipherSpec message since all data from then on is encrypted.

    :param data:
        A byte string of TLS records

    :return:
        A generator that yields 3-element tuples:
        [0] Byte string of record type
        [1] Byte string of protocol version
        [2] Byte string of record data
    """

    pointer = 0
    data_len = len(data)
    while pointer < data_len:
        # Don't try to parse any more once the ChangeCipherSpec is found
        if data[pointer:pointer + 1] == b'\x14':
            break
        length = int_from_bytes(data[pointer + 3:pointer + 5])
        yield (
            data[pointer:pointer + 1],
            data[pointer + 1:pointer + 3],
            data[pointer + 5:pointer + 5 + length]
        )
        pointer += 5 + length