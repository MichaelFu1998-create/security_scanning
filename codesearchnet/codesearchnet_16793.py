def add_arguments(parser):
    """
    Args for the init command
    """
    parser.add_argument('-e', '--environment',  help='Environment name', required=False, nargs='+')
    parser.add_argument('-w', '--dont-wait', help='Skip waiting for the app to be deleted', action='store_true')