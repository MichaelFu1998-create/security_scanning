def add_newlines(f, output, char):
    """Adds line breaks after every occurance of a given character in a file.

    Args:
        f: string, path to input file.

        output: string, path to output file.

    Returns:
        None.
    """
    line_count = get_line_count(f)
    f = open(f, 'r+')
    output = open(output, 'r+')
    for line in range(line_count):
        string = f.readline()
        string = re.sub(char, char + '\n', string)
        output.write(string)