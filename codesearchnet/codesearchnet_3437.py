def hr_size(num, suffix='B') -> str:
    """
    Human-readable data size
    From https://stackoverflow.com/a/1094933
    :param num: number of bytes
    :param suffix: Optional size specifier
    :return: Formatted string
    """
    for unit in ' KMGTPEZ':
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit if unit != ' ' else '', suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)