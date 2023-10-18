def _load_packets(file_h, header, layers=0):
    """
    Read packets from the capture file. Expects the file handle to point to
    the location immediately after the header (24 bytes).
    """
    pkts = []

    hdrp = ctypes.pointer(header)
    while True:
        pkt = _read_a_packet(file_h, hdrp, layers)
        if pkt:
            pkts.append(pkt)
        else:
            break

    return pkts