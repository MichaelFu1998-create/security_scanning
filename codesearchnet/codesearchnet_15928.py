def _read_a_packet(file_h, hdrp, layers=0):
    """
    Reads the next individual packet from the capture file. Expects
    the file handle to be somewhere after the header, on the next
    per-packet header.
    """
    raw_packet_header = file_h.read(16)
    if not raw_packet_header or len(raw_packet_header) != 16:
        return None

    # in case the capture file is not the same endianness as ours, we have to
    # use the correct byte order for the packet header
    if hdrp[0].byteorder == 'big':
        packet_header = struct.unpack('>IIII', raw_packet_header)
    else:
        packet_header = struct.unpack('<IIII', raw_packet_header)
    (timestamp, timestamp_us, capture_len, packet_len) = packet_header
    raw_packet_data = file_h.read(capture_len)

    if not raw_packet_data or len(raw_packet_data) != capture_len:
        return None

    if layers > 0:
        layers -= 1
        raw_packet = linklayer.clookup(hdrp[0].ll_type)(raw_packet_data,
                                                        layers=layers)
    else:
        raw_packet = raw_packet_data

    packet = pcap_packet(hdrp, timestamp, timestamp_us, capture_len,
                         packet_len, raw_packet)
    return packet