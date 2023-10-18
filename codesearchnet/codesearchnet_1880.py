def pformat(o, indent=1, width=80, depth=None):
    """Format a Python o into a pretty-printed representation."""
    return PrettyPrinter(indent=indent, width=width, depth=depth).pformat(o)