def bump():
    """ CLI entry point to bump requirements in requirements.txt or pinned.txt """

    parser = argparse.ArgumentParser(description=bump.__doc__)
    parser.add_argument('names', nargs='*', help="""
      Only bump dependencies that match the name.
      Name can be a product group name defined in workspace.cfg.
      To bump to a specific version instead of latest, append version to name
      (i.e. requests==1.2.3 or 'requests>=1.2.3'). When > or < is used, be sure to quote.""")
    parser.add_argument('--add', '--require', action='store_true',
                        help='Add the `names` to the requirements file if they don\'t exist.')
    parser.add_argument('--file', help='Requirement file to bump. Defaults to requirements.txt and pinned.txt')
    parser.add_argument('--force', action='store_true',
                        help='Force a bump even when certain bump requirements are not met.')
    parser.add_argument('-d', '--detail', '--dependencies', action='store_true',
                        help='If available, show detailed changes. '
                             'For pinned.txt, pin parsed dependency requirements from changes')
    parser.add_argument('-n', '--dry-run', action='store_true', help='Perform a dry run without making changes')
    parser.add_argument('--debug', action='store_true', help='Turn on debug mode')

    args = parser.parse_args()
    targets = [args.file] if args.file else ['requirements.txt', 'pinned.txt']

    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=level, format='[%(levelname)s] %(message)s')

    try:
        bumper = BumperDriver(targets, full_throttle=args.force, detail=args.detail, test_drive=args.dry_run)
        bumper.bump(args.names, required=args.add, show_detail=args.detail)
    except Exception as e:
        if args.debug:
            raise
        else:
            log.error(e)
            sys.exit(1)