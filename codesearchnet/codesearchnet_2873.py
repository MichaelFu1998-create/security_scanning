def create_packet(header, data):
    """Creates an IncomingPacket object from header and data

    This method is for testing purposes
    """
    packet = IncomingPacket()
    packet.header = header
    packet.data = data

    if len(header) == HeronProtocol.HEADER_SIZE:
      packet.is_header_read = True
      if len(data) == packet.get_datasize():
        packet.is_complete = True

    return packet