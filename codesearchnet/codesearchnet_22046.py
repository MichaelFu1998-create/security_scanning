def main(args=sys.argv[1:]):
    '''Processes command line arguments and file i/o'''
    if not args:
        sys.stderr.write(_usage() + '\n')
        sys.exit(4)
    else:
        parsed = _parse_args(args)

    # Set delim based on whether or not regex is desired by user
    delim = parsed.delimiter if parsed.regex else re.escape(parsed.delimiter)

    # Keep track of number of cutters used to allow error handling if
    # multiple options selected (only one at a time is accepted)
    num_cutters = 0

    # Read mode will be used as file read mode later. 'r' is default, changed
    # to 'rb' in the event that binary read mode is selected by user
    read_mode = 'r'

    if parsed.bytes:
        positions = parsed.bytes
        cutter = ByteCutter(positions)
        num_cutters += 1
        read_mode = 'rb'

    if parsed.chars:
        positions = parsed.chars
        cutter = CharCutter(positions)
        num_cutters += 1

    if parsed.fields:
        positions = parsed.fields
        cutter = FieldCutter(positions, delim, parsed.separator)
        num_cutters += 1

    # Make sure only one option of -b,-c, or -f is used
    if num_cutters > 1:
        sys.stderr.write('Only one option permitted of -b, -c, -f.\n')
        sys.stderr.write(_usage() + '\n')
        sys.exit(1)

    # Check for possible specification of zero index, which is not allowed.
    # Regular expression checks for zero by itself, or in range specification
    if [n for n in positions if re.search("0:?|0$", n)]:
        sys.stderr.write('Zero is an invalid position.\n')
        sys.stderr.write(_usage() + '\n')
        sys.exit(2)


    try:
        for line in fileinput.input(parsed.file, mode=read_mode):
            if parsed.skip and not re.search(parsed.delimiter, line):
                pass
            else:
                # Using sys.stdout.write for consistency between Py 2 and 3,
                # keeping linter happy
                print(cutter.cut(line))
    except IOError:
        sys.stderr.write('File \'' + fileinput.filename()
                         + '\' could not be found.\n')
        sys.exit(3)

    fileinput.close()