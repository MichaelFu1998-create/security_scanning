def has_address(start: int, data_length: int) -> bool:
    """
    Determine whether the packet has an "address" encoded into it.
    There exists an undocumented bug/edge case in the spec - some packets
    with 0x82 as _start_, still encode the address into the packet, and thus
    throws off decoding. This edge case is handled explicitly.
    """
    return bool(0x01 & start) or (start == 0x82 and data_length == 16)