def add_arguments(parser):
    """
    adds arguments for the deploy command
    """
    parser.add_argument('-e', '--environment',      help='Environment name', required=True)
    parser.add_argument('-w', '--dont-wait',        help='Skip waiting for the init to finish', action='store_true')
    parser.add_argument('-l', '--version-label',    help='Version label', required=False)