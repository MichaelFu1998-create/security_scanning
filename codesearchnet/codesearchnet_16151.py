def byteswap(fmt, data, offset=0):
    """Swap bytes in `data` according to `fmt`, starting at byte `offset`
    and return the result. `fmt` must be an iterable, iterating over
    number of bytes to swap. For example, the format string ``'24'``
    applied to the bytes ``b'\\x00\\x11\\x22\\x33\\x44\\x55'`` will
    produce the result ``b'\\x11\\x00\\x55\\x44\\x33\\x22'``.

    """

    data = BytesIO(data)
    data.seek(offset)
    data_swapped = BytesIO()

    for f in fmt:
        swapped = data.read(int(f))[::-1]
        data_swapped.write(swapped)

    return data_swapped.getvalue()