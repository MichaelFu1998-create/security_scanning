def create_packet(reqid, message):
    """Creates Outgoing Packet from a given reqid and message

    :param reqid: REQID object
    :param message: protocol buffer object
    """
    assert message.IsInitialized()
    packet = ''

    # calculate the totla size of the packet incl. header
    typename = message.DESCRIPTOR.full_name

    datasize = HeronProtocol.get_size_to_pack_string(typename) + \
               REQID.REQID_SIZE + HeronProtocol.get_size_to_pack_message(message)

    # first write out how much data is there as the header
    packet += HeronProtocol.pack_int(datasize)

    # next write the type string
    packet += HeronProtocol.pack_int(len(typename))
    packet += typename

    # reqid
    packet += reqid.pack()

    # add the proto
    packet += HeronProtocol.pack_int(message.ByteSize())
    packet += message.SerializeToString()
    return OutgoingPacket(packet)