def read_stream(schema, stream, *, buffer_size=io.DEFAULT_BUFFER_SIZE):
    """Using a schema, deserialize a stream of consecutive Avro values.

    :param str schema: json string representing the Avro schema
    :param file-like stream: a buffered stream of binary input
    :param int buffer_size: size of bytes to read from the stream each time
    :return: yields a sequence of python data structures deserialized
        from the stream

    """
    reader = _lancaster.Reader(schema)
    buf = stream.read(buffer_size)
    remainder = b''
    while len(buf) > 0:
        values, n = reader.read_seq(buf)
        yield from values
        remainder = buf[n:]
        buf = stream.read(buffer_size)
        if len(buf) > 0 and len(remainder) > 0:
            ba = bytearray()
            ba.extend(remainder)
            ba.extend(buf)
            buf = memoryview(ba).tobytes()
    if len(remainder) > 0:
        raise EOFError('{} bytes remaining but could not continue reading '
                       'from stream'.format(len(remainder)))