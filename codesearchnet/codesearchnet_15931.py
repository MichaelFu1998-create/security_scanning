def strip_ethernet(packet):
    """
    Strip the Ethernet frame from a packet.
    """
    if not isinstance(packet, Ethernet):
        packet = Ethernet(packet)
    payload = packet.payload

    return payload