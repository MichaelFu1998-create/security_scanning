def get_params():
    """Get params to execute the micro-mordred"""

    parser = get_params_parser()
    args = parser.parse_args()

    if not args.raw and not args.enrich and not args.identities and not args.panels:
        print("No tasks enabled")
        sys.exit(1)

    return args