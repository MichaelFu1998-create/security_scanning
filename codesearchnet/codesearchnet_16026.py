def _arg_parser():
    """Factory for creating the argument parser"""
    description = "Converts a completezip to a litezip"
    parser = argparse.ArgumentParser(description=description)
    verbose_group = parser.add_mutually_exclusive_group()
    verbose_group.add_argument(
        '-v', '--verbose', action='store_true',
        dest='verbose', default=None,
        help="increase verbosity")
    verbose_group.add_argument(
        '-q', '--quiet', action='store_false',
        dest='verbose', default=None,
        help="print nothing to stdout or stderr")
    parser.add_argument(
        'location',
        help="Location of the unpacked litezip")
    return parser