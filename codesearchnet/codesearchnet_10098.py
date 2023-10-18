def _convert_filetime_to_timestamp(filetime):
    """
    Windows returns times as 64-bit unsigned longs that are the number
    of hundreds of nanoseconds since Jan 1 1601. This converts it to
    a datetime object.

    :param filetime:
        A FILETIME struct object

    :return:
        An integer unix timestamp
    """

    hundreds_nano_seconds = struct.unpack(
        b'>Q',
        struct.pack(
            b'>LL',
            filetime.dwHighDateTime,
            filetime.dwLowDateTime
        )
    )[0]
    seconds_since_1601 = hundreds_nano_seconds / 10000000
    return seconds_since_1601 - 11644473600