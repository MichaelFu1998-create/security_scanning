def parse_ipv4(address):
    """
    Given a raw IPv4 address (i.e. as an unsigned integer), return it in
    dotted quad notation.
    """
    raw = struct.pack('I', address)
    octets = struct.unpack('BBBB', raw)[::-1]
    ipv4 = b'.'.join([('%d' % o).encode('ascii') for o in bytearray(octets)])
    return ipv4