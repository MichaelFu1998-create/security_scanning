def main():
    """Parse the command-line arguments and run the bot."""
    parser = argparse.ArgumentParser(description = 'XMPP echo bot',
                                    parents = [XMPPSettings.get_arg_parser()])
    parser.add_argument('jid', metavar = 'JID', 
                                        help = 'The bot JID')
    parser.add_argument('--debug',
                        action = 'store_const', dest = 'log_level',
                        const = logging.DEBUG, default = logging.INFO,
                        help = 'Print debug messages')
    parser.add_argument('--quiet', const = logging.ERROR,
                        action = 'store_const', dest = 'log_level',
                        help = 'Print only error messages')
    parser.add_argument('--trace', action = 'store_true',
                        help = 'Print XML data sent and received')

    args = parser.parse_args()
    settings = XMPPSettings({
                            "software_name": "Echo Bot"
                            })
    settings.load_arguments(args)

    if settings.get("password") is None:
        password = getpass("{0!r} password: ".format(args.jid))
        if sys.version_info.major < 3:
            password = password.decode("utf-8")
        settings["password"] = password

    if sys.version_info.major < 3:
        args.jid = args.jid.decode("utf-8")

    logging.basicConfig(level = args.log_level)
    if args.trace:
        print "enabling trace"
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        for logger in ("pyxmpp2.IN", "pyxmpp2.OUT"):
            logger = logging.getLogger(logger)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)
            logger.propagate = False

    bot = EchoBot(JID(args.jid), settings)
    try:
        bot.run()
    except KeyboardInterrupt:
        bot.disconnect()