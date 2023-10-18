def _show_warning(message, category, filename, lineno, file=None, line=None):
    """Hook to write a warning to a file; replace if you like."""
    if file is None:
        file = sys.stderr
        if file is None:
            # sys.stderr is None - warnings get lost
            return
    try:
        file.write(formatwarning(message, category, filename, lineno, line))
    except (IOError, UnicodeError):
        pass # the file (probably stderr) is invalid - this warning gets lost.