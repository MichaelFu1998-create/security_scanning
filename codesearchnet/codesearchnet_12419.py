def address(addr, label=None):
    """Discover the proper class and return instance for a given Monero address.

    :param addr: the address as a string-like object
    :param label: a label for the address (defaults to `None`)

    :rtype: :class:`Address`, :class:`SubAddress` or :class:`IntegratedAddress`
    """
    addr = str(addr)
    if _ADDR_REGEX.match(addr):
        netbyte = bytearray(unhexlify(base58.decode(addr)))[0]
        if netbyte in Address._valid_netbytes:
            return Address(addr, label=label)
        elif netbyte in SubAddress._valid_netbytes:
            return SubAddress(addr, label=label)
        raise ValueError("Invalid address netbyte {nb:x}. Allowed values are: {allowed}".format(
            nb=netbyte,
            allowed=", ".join(map(
                lambda b: '%02x' % b,
                sorted(Address._valid_netbytes + SubAddress._valid_netbytes)))))
    elif _IADDR_REGEX.match(addr):
        return IntegratedAddress(addr)
    raise ValueError("Address must be either 95 or 106 characters long base58-encoded string, "
        "is {addr} ({len} chars length)".format(addr=addr, len=len(addr)))