def get_params_parser():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('-g', '--debug', dest='debug',
                        action='store_true',
                        help=argparse.SUPPRESS)
    parser.add_argument("--arthur", action='store_true', dest='arthur',
                        help="Enable arthur to collect raw data")
    parser.add_argument("--raw", action='store_true', dest='raw',
                        help="Activate raw task")
    parser.add_argument("--enrich", action='store_true', dest='enrich',
                        help="Activate enrich task")
    parser.add_argument("--identities", action='store_true', dest='identities',
                        help="Activate merge identities task")
    parser.add_argument("--panels", action='store_true', dest='panels',
                        help="Activate panels task")

    parser.add_argument("--cfg", dest='cfg_path',
                        help="Configuration file path")
    parser.add_argument("--backends", dest='backend_sections', default=[],
                        nargs='*', help="Backend sections to execute")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser