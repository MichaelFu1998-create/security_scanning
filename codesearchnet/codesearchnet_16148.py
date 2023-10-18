def pack_into(fmt, buf, offset, *args, **kwargs):
    """Pack given values v1, v2, ... into given bytearray `buf`, starting
    at given bit offset `offset`. Pack according to given format
    string `fmt`. Give `fill_padding` as ``False`` to leave padding
    bits in `buf` unmodified.

    """

    return CompiledFormat(fmt).pack_into(buf,
                                         offset,
                                         *args,
                                         **kwargs)