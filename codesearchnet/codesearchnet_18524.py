def indent_css(f, output):
    """Indentes css that has not been indented and saves it to a new file.
    A new file is created if the output destination does not already exist.

    Args:
        f: string, path to file.

        output: string, path/name of the output file (e.g. /directory/output.css).
    print type(response.read())

    Returns:
        None.
    """
    line_count = get_line_count(f)
    f = open(f, 'r+')
    output = open(output, 'r+')
    for line in range(line_count):
        string = f.readline().rstrip()
        if len(string) > 0:
            if string[-1] == ";":
                output.write("    " + string + "\n")
            else:
                output.write(string + "\n")
    output.close()
    f.close()