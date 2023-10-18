def _add_redundant_arguments(parser):
    """
    These arguments are redundant with just using a project, and we should
    encouraging that as you don't have to learn any dumb flags!

    For example, instead of

       bp foo.yml --animation=wombat --numbers=float

    use

       bp foo.yml + '{animation: wombat, numbers: float}'

    """
    parser.add_argument(
        '-a', '--animation', default=None,
        help='Default animation type if no animation is specified')

    if deprecated.allowed():  # pragma: no cover
        parser.add_argument(
            '--dimensions', '--dim', default=None,
            help='DEPRECATED: x, (x, y) or (x, y, z) dimensions for project')

    parser.add_argument(
        '--shape', default=None,
        help='x, (x, y) or (x, y, z) dimensions for project')

    parser.add_argument(
        '-l', '--layout', default=None,
        help='Default layout class if no layout is specified')

    parser.add_argument(
        '--numbers', '-n', default='python', choices=NUMBER_TYPES,
        help=NUMBERS_HELP)

    parser.add_argument('-p', '--path', default=None, help=PATH_HELP)