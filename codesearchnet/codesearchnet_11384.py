def usage_function(parser):
    """Show usage and available curve functions."""
    parser.print_usage()
    print('')
    print('available functions:')
    for function in sorted(FUNCTION):
        doc = FUNCTION[function].__doc__.strip().splitlines()[0]
        print('    %-12s %s' % (function + ':', doc))

    return 0