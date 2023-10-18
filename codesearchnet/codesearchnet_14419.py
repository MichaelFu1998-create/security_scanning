def main():
    """
    Main script for `pyconfig` command.

    """
    parser = argparse.ArgumentParser(description="Helper for working with "
            "pyconfigs")
    target_group = parser.add_mutually_exclusive_group()
    target_group.add_argument('-f', '--filename',
            help="parse an individual file or directory",
            metavar='F')
    target_group.add_argument('-m', '--module',
            help="parse a package or module, recursively looking inside it",
            metavar='M')
    parser.add_argument('-v', '--view-call',
            help="show the actual pyconfig call made (default: show namespace)",
            action='store_true')
    parser.add_argument('-l', '--load-configs',
            help="query the currently set value for each key found",
            action='store_true')
    key_group = parser.add_mutually_exclusive_group()
    key_group.add_argument('-a', '--all',
            help="show keys which don't have defaults set",
            action='store_true')
    key_group.add_argument('-k', '--only-keys',
            help="show a list of discovered keys without values",
            action='store_true')
    parser.add_argument('-n', '--natural-sort',
            help="sort by filename and line (default: alphabetical by key)",
            action='store_true')
    parser.add_argument('-s', '--source',
            help="show source annotations (implies --natural-sort)",
            action='store_true')
    parser.add_argument('-c', '--color',
            help="toggle output colors (default: %s)" % bool(pygments),
            action='store_const', default=bool(pygments),
            const=(not bool(pygments)))
    args = parser.parse_args()

    if args.color and not pygments:
        _error("Pygments is required for color output.\n"
                "    pip install pygments")

    if args.module:
        _handle_module(args)

    if args.filename:
        _handle_file(args)