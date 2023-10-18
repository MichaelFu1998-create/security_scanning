def main():
    """Parse the command-line arguments and run the tool."""
    parser = argparse.ArgumentParser(description = 'XMPP version checker',
                                    parents = [XMPPSettings.get_arg_parser()])
    parser.add_argument('source', metavar = 'SOURCE', 
                                        help = 'Source JID')
    parser.add_argument('target', metavar = 'TARGET', nargs = '?',
                            help = 'Target JID (default: domain of SOURCE)')
    parser.add_argument('--debug',
                        action = 'store_const', dest = 'log_level',
                        const = logging.DEBUG, default = logging.INFO,
                        help = 'Print debug messages')
    parser.add_argument('--quiet', const = logging.ERROR,
                        action = 'store_const', dest = 'log_level',
                        help = 'Print only error messages')
    args = parser.parse_args()
    settings = XMPPSettings()
    settings.load_arguments(args)
    
    if settings.get("password") is None:
        password = getpass("{0!r} password: ".format(args.source))
        if sys.version_info.major < 3:
            password = password.decode("utf-8")
        settings["password"] = password

    if sys.version_info.major < 3:
        args.source = args.source.decode("utf-8")

    source = JID(args.source)

    if args.target:
        if sys.version_info.major < 3:
            args.target = args.target.decode("utf-8")
        target = JID(args.target)
    else:
        target = JID(source.domain)

    logging.basicConfig(level = args.log_level)

    checker = VersionChecker(source, target, settings)
    try:
        checker.run()
    except KeyboardInterrupt:
        checker.disconnect()