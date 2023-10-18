def error(message):
    '''Prints an error message, the help message and quits'''
    global parser
    print (_("Error: ") + message)
    print ()
    parser.print_help()
    sys.exit()