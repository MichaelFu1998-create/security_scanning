def reformat_css(input_file, output_file):
    """Reformats poorly written css. This function does not validate or fix errors in the code.
    It only gives code the proper indentation. 

    Args:
        input_file: string, path to the input file.

        output_file: string, path to where the reformatted css should be saved. If the target file
        doesn't exist, a new file is created.

    Returns:
        None.
    """
    # Number of lines in the file.
    line_count = get_line_count(input_file)

    # Open source and target files.
    f = open(input_file, 'r+')
    output = open(output_file, 'w')

    # Loop over every line in the file.
    for line in range(line_count):
        # Eliminate whitespace at the beginning and end of lines.
        string = f.readline().strip()
        # New lines after { 
        string = re.sub('\{', '{\n', string)
        # New lines after ; 
        string = re.sub('; ', ';', string)
        string = re.sub(';', ';\n', string)
        # Eliminate whitespace before comments
        string = re.sub('} /*', '}/*', string)
        # New lines after } 
        string = re.sub('\}', '}\n', string)
        # New lines at the end of comments
        string = re.sub('\*/', '*/\n', string)
        # Write to the output file.
        output.write(string)

    # Close the files.
    output.close()
    f.close()

    # Indent the css.
    indent_css(output_file, output_file)

    # Make sure there's a space before every {
    add_whitespace_before("{", output_file, output_file)