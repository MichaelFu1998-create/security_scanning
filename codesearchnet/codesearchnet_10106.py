def _parse_hello_extensions(data):
    """
    Creates a generator returning tuples of information about each extension
    from a byte string of extension data contained in a ServerHello ores
    ClientHello message

    :param data:
        A byte string of a extension data from a TLS ServerHello or ClientHello
        message

    :return:
        A generator that yields 2-element tuples:
        [0] Byte string of extension type
        [1] Byte string of extension data
    """

    if data == b'':
        return

    extentions_length = int_from_bytes(data[0:2])
    extensions_start = 2
    extensions_end = 2 + extentions_length

    pointer = extensions_start
    while pointer < extensions_end:
        extension_type = int_from_bytes(data[pointer:pointer + 2])
        extension_length = int_from_bytes(data[pointer + 2:pointer + 4])
        yield (
            extension_type,
            data[pointer + 4:pointer + 4 + extension_length]
        )
        pointer += 4 + extension_length