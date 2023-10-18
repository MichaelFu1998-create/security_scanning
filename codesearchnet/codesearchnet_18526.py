def add_whitespace_before(char, input_file, output_file):
    """Adds a space before a character if there's isn't one already.
    
    Args:
        char: string, character that needs a space before it.

        input_file: string, path to file to parse.

        output_file: string, path to destination file.
    
    Returns:
        None.
    """
    line_count = get_line_count(input_file)
    input_file = open(input_file, 'r')
    output_file = open(output_file, 'r+')
    for line in range(line_count):
        string = input_file.readline()
        # If there's not already a space before the character, add one
        if re.search(r'[a-zA-Z0-9]' + char, string) != None:
            string = re.sub(char, ' ' + char, string)
        output_file.write(string)
    input_file.close()