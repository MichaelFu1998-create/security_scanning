def lint_file(in_file, out_file=None):
    """Helps remove extraneous whitespace from the lines of a file

    :param file in_file: A readable file or file-like
    :param file out_file: A writable file or file-like
    """
    for line in in_file:
        print(line.strip(), file=out_file)