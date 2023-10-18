def print_list(extracted_list, file=None):
    """Print the list of tuples as returned by extract_tb() or
    extract_stack() as a formatted stack trace to the given file."""
    if file is None:
        file = sys.stderr
    for filename, lineno, name, line in extracted_list:
        _print(file,
               '  File "%s", line %d, in %s' % (filename,lineno,name))
        if line:
            _print(file, '    %s' % line.strip())