def parse_defines(args):
    """
    This parses a list of define argument in the form of -DNAME=VALUE or -DNAME (
    which is treated as -DNAME=1).
    """
    macros = {}
    for arg in args:
        try:
            var, val = arg.split('=', 1)
        except ValueError:
            var = arg
            val = '1'

        macros[var] = val

    return macros