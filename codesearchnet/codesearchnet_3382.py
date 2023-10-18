def main():
    """
    Dispatches execution into one of Manticore's engines: evm or native.
    """
    args = parse_arguments()

    if args.no_colors:
        log.disable_colors()

    sys.setrecursionlimit(consts.recursionlimit)

    ManticoreBase.verbosity(args.v)

    if args.argv[0].endswith('.sol'):
        ethereum_main(args, logger)
    else:
        install_helper.ensure_native_deps()
        native_main(args, logger)