def add_arguments(parser):
    """
    adds arguments for the swap urls command
    """
    parser.add_argument('-o', '--old-environment', help='Old environment name', required=True)
    parser.add_argument('-n', '--new-environment', help='New environment name', required=True)