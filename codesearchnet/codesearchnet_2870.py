def decode_packet(packet):
    """Decodes an IncomingPacket object and returns (typename, reqid, serialized message)"""
    if not packet.is_complete:
      raise RuntimeError("In decode_packet(): Packet corrupted")

    data = packet.data

    len_typename = HeronProtocol.unpack_int(data[:4])
    data = data[4:]

    typename = data[:len_typename]
    data = data[len_typename:]

    reqid = REQID.unpack(data[:REQID.REQID_SIZE])
    data = data[REQID.REQID_SIZE:]

    len_msg = HeronProtocol.unpack_int(data[:4])
    data = data[4:]

    serialized_msg = data[:len_msg]

    return typename, reqid, serialized_msg