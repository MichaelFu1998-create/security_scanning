def dostime_to_timetuple(dostime):
    """Convert a RAR archive member DOS time to a Python time tuple."""
    dostime = dostime >> 16
    dostime = dostime & 0xffff
    day = dostime & 0x1f
    month = (dostime >> 5) & 0xf
    year = 1980 + (dostime >> 9)
    second = 2 * (dostime & 0x1f)
    minute = (dostime >> 5) & 0x3f
    hour = dostime >> 11
    return (year, month, day, hour, minute, second)