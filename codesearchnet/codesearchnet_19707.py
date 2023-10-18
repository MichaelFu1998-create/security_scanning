def _dec_to_bin(ip):
    """Decimal to binary conversion."""
    bits = []
    while ip:
        bits.append(_BYTES_TO_BITS[ip & 255])
        ip >>= 8
    bits.reverse()
    return ''.join(bits) or 32*'0'