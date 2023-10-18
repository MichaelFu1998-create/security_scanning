def add_arguments(parser):
    """
    adds arguments for the deploy command
    """
    parser.add_argument('-e', '--environment', help='Environment name', required=True)
    parser.add_argument('-w', '--dont-wait', help='Skip waiting', action='store_true')
    parser.add_argument('-a', '--archive', help='Archive file', required=False)
    parser.add_argument('-d', '--directory', help='Directory', required=False)
    parser.add_argument('-l', '--version-label', help='Version label', required=False)
    parser.add_argument('-t', '--termination-delay',
                        help='Delay termination of old environment by this number of seconds',
                        type=int, required=False)