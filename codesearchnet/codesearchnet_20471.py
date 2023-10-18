def parse_args(args):
    """
    Parse args from command line by creating argument parser instance and
    process it.

    :param args: Command line arguments list.
    """
    from argparse import ArgumentParser

    description = ('Bootstrap Python projects and libraries with virtualenv '
                   'and pip.')
    parser = ArgumentParser(description=description)
    parser.add_argument('--version', action='version', version=__version__)

    parser.add_argument(
        '-c', '--config', default=DEFAULT_CONFIG,
        help='Path to config file. By default: {0}'.format(DEFAULT_CONFIG)
    )
    parser.add_argument(
        '-p', '--pre-requirements', default=[], nargs='+',
        help='List of pre-requirements to check, separated by space.'
    )
    parser.add_argument(
        '-e', '--env',
        help='Virtual environment name. By default: {0}'.
             format(CONFIG[__script__]['env'])
    )
    parser.add_argument(
        '-r', '--requirements',
        help='Path to requirements file. By default: {0}'.
             format(CONFIG[__script__]['requirements'])
    )
    parser.add_argument(
        '-d', '--install-dev-requirements', action='store_true', default=None,
        help='Install prefixed or suffixed "dev" requirements after '
             'installation of original requirements file or library completed '
             'without errors.'
    )
    parser.add_argument(
        '-C', '--hook', help='Execute this hook after bootstrap process.'
    )
    parser.add_argument(
        '--ignore-activated', action='store_true', default=None,
        help='Ignore pre-activated virtualenv, like on Travis CI.'
    )
    parser.add_argument(
        '--recreate', action='store_true', default=None,
        help='Recreate virtualenv on every run.'
    )
    parser.add_argument(
        '-q', '--quiet', action='store_true', default=None,
        help='Minimize output, show only error messages.'
    )

    return parser.parse_args(args)