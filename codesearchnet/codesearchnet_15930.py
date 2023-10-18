def strip_ip(packet):
    """
    Remove the IP packet layer, yielding the transport layer.
    """
    if not isinstance(packet, IP):
        packet = IP(packet)
    payload = packet.payload

    return payload