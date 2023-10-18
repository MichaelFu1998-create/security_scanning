def byte_number_string(
    number, thousandsSep=True, partition=False, base1024=True, appendBytes=True
):
    """Convert bytes into human-readable representation."""
    magsuffix = ""
    bytesuffix = ""

    if partition:
        magnitude = 0
        if base1024:
            while number >= 1024:
                magnitude += 1
                number = number >> 10
        else:
            while number >= 1000:
                magnitude += 1
                number /= 1000.0
        # TODO: use "9 KB" instead of "9K Bytes"?
        # TODO use 'kibi' for base 1024?
        # http://en.wikipedia.org/wiki/Kibi-#IEC_standard_prefixes
        magsuffix = ["", "K", "M", "G", "T", "P"][magnitude]

    if appendBytes:
        if number == 1:
            bytesuffix = " Byte"
        else:
            bytesuffix = " Bytes"

    if thousandsSep and (number >= 1000 or magsuffix):
        # locale.setlocale(locale.LC_ALL, "")
        # # TODO: make precision configurable
        # snum = locale.format("%d", number, thousandsSep)
        snum = "{:,d}".format(number)
    else:
        snum = str(number)

    return "{}{}{}".format(snum, magsuffix, bytesuffix)