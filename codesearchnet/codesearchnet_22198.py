def formatter(color, s):
    """ Formats a string with color """
    if no_coloring:
        return s
    return "{begin}{s}{reset}".format(begin=color, s=s, reset=Colors.RESET)