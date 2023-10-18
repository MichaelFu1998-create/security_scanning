def pprint(o, stream=None, indent=1, width=80, depth=None):
    """Pretty-print a Python o to a stream [default is sys.stdout]."""
    printer = PrettyPrinter(
        stream=stream, indent=indent, width=width, depth=depth)
    printer.pprint(o)