def main():
    """Parse the command-line arguments and run the bot."""
    parser = argparse.ArgumentParser(description = 'XMPP echo bot',
                                    parents = [XMPPSettings.get_arg_parser()])
    parser.add_argument('--debug',
                        action = 'store_const', dest = 'log_level',
                        const = logging.DEBUG, default = logging.INFO,
                        help = 'Print debug messages')
    parser.add_argument('--quiet', const = logging.ERROR,
                        action = 'store_const', dest = 'log_level',
                        help = 'Print only error messages')
    parser.add_argument('--trace', action = 'store_true',
                        help = 'Print XML data sent and received')
    parser.add_argument('--roster-cache', 
                        help = 'Store roster in this file')
    parser.add_argument('jid', metavar = 'JID', 
                                        help = 'The bot JID')
    subparsers = parser.add_subparsers(help = 'Action', dest = "action")
    show_p = subparsers.add_parser('show', help = 'Show roster and exit')
    show_p.add_argument('--presence', action = 'store_true',
                        help = 'Wait 5 s for contact presence information'
                                ' and display it with the roster')
    mon_p = subparsers.add_parser('monitor', help = 
                                        'Show roster and subsequent changes')
    mon_p.add_argument('--presence', action = 'store_true',
                        help = 'Show contact presence changes too')
    add_p = subparsers.add_parser('add', help = 'Add an item to the roster')
    add_p.add_argument('--subscribe', action = 'store_true', dest = 'subscribe',
                        help = 'Request a presence subscription too')
    add_p.add_argument('--approve', action = 'store_true', dest = 'approve',
                        help = 'Pre-approve subscription from the contact'
                                                ' (requires server support)')
    add_p.add_argument('contact', metavar = 'CONTACT', help = 'The JID to add')
    add_p.add_argument('name', metavar = 'NAME', nargs = '?',
                                            help = 'Contact name')
    add_p.add_argument('groups', metavar = 'GROUP', nargs = '*',
                                            help = 'Group names')
    rm_p = subparsers.add_parser('remove',
                                    help = 'Remove an item from the roster')
    rm_p.add_argument('contact', metavar = 'CONTACT',
                                    help = 'The JID to remove')
    upd_p = subparsers.add_parser('update', 
                                    help = 'Update an item in the roster')
    upd_p.add_argument('contact', metavar = 'CONTACT',
                                    help = 'The JID to update')
    upd_p.add_argument('name', metavar = 'NAME', nargs = '?',
                                            help = 'Contact name')
    upd_p.add_argument('groups', metavar = 'GROUP', nargs = '*',
                                            help = 'Group names')

    args = parser.parse_args()
    settings = XMPPSettings()
    settings.load_arguments(args)

    if settings.get("password") is None:
        password = getpass("{0!r} password: ".format(args.jid))
        if sys.version_info.major < 3:
            password = password.decode("utf-8")
        settings["password"] = password

    if sys.version_info.major < 3:
        args.jid = args.jid.decode("utf-8")
        if getattr(args, "contact", None):
            args.contact = args.contact.decode("utf-8")
        if getattr(args, "name", None):
            args.name = args.name.decode("utf-8")
        if getattr(args, "groups", None):
            args.groups = [g.decode("utf-8") for g in args.groups]

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
           
    if args.action == "monitor" or args.action == "show" and args.presence:
        # According to RFC6121 it could be None for 'monitor' (no need to send
        # initial presence to request roster), but Google seems to require that
        # to send roster pushes
        settings["initial_presence"] = Presence(priority = -1)
    else:
        settings["initial_presence"] = None

    tool = RosterTool(JID(args.jid), args, settings)
    try:
        tool.run()
    except KeyboardInterrupt:
        tool.disconnect()