def _usage(prog_name=os.path.basename(sys.argv[0])):
    '''Returns usage string with no trailing whitespace.'''
    spacer = ' ' * len('usage: ')
    usage = prog_name + ' -b LIST [-S SEPARATOR] [file ...]\n' \
       + spacer + prog_name + ' -c LIST [-S SEPERATOR] [file ...]\n' \
       + spacer + prog_name \
       + ' -f LIST [-d DELIM] [-e] [-S SEPERATOR] [-s] [file ...]'

    # Return usage message with trailing whitespace removed.
    return "usage: " + usage.rstrip()