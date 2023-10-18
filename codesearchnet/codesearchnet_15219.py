def decode_timestamp(data: str) -> datetime.datetime:
    """
    Decode timestamp using bespoke decoder.
    Cannot use simple strptime since the ness panel contains a bug
    that P199E zone and state updates emitted on the hour cause a minute
    value of `60` to be sent, causing strptime to fail. This decoder handles
    this edge case.
    """
    year = 2000 + int(data[0:2])
    month = int(data[2:4])
    day = int(data[4:6])
    hour = int(data[6:8])
    minute = int(data[8:10])
    second = int(data[10:12])
    if minute == 60:
        minute = 0
        hour += 1

    return datetime.datetime(year=year, month=month, day=day, hour=hour,
                             minute=minute, second=second)