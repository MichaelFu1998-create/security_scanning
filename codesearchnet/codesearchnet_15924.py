def _load_savefile_header(file_h):
    """
    Load and validate the header of a pcap file.
    """
    try:
        raw_savefile_header = file_h.read(24)
    except UnicodeDecodeError:
        print("\nMake sure the input file is opened in read binary, 'rb'\n")
        raise InvalidEncoding("Could not read file; it might not be opened in binary mode.")

    # in case the capture file is not the same endianness as ours, we have to
    # use the correct byte order for the file header
    if raw_savefile_header[:4] in [struct.pack(">I", _MAGIC_NUMBER),
                                   struct.pack(">I", _MAGIC_NUMBER_NS)]:
        byte_order = b'big'
        unpacked = struct.unpack('>IhhIIII', raw_savefile_header)
    elif raw_savefile_header[:4] in [struct.pack("<I", _MAGIC_NUMBER),
                                     struct.pack("<I", _MAGIC_NUMBER_NS)]:
        byte_order = b'little'
        unpacked = struct.unpack('<IhhIIII', raw_savefile_header)
    else:
        raise UnknownMagicNumber("No supported Magic Number found")

    (magic, major, minor, tz_off, ts_acc, snaplen, ll_type) = unpacked
    header = __pcap_header__(magic, major, minor, tz_off, ts_acc, snaplen,
                             ll_type, ctypes.c_char_p(byte_order),
                             magic == _MAGIC_NUMBER_NS)
    if not __validate_header__(header):
        raise InvalidHeader("Invalid Header")
    else:
        return header