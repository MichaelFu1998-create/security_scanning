def argparser():
    """Constructs the ArgumentParser for the CLI"""

    parser = ArgumentParser(prog='pynetgear')

    parser.add_argument("--format", choices=['json', 'prettyjson', 'py'], default='prettyjson')

    router_args = parser.add_argument_group("router connection config")
    router_args.add_argument("--host", help="Hostname for the router")
    router_args.add_argument("--user", help="Account for login")
    router_args.add_argument("--port", help="Port exposed on the router")
    router_args.add_argument("--login-v2", help="Force the use of the cookie-based authentication",
                             dest="force_login_v2", default=False, action="store_true")
    router_args.add_argument(
            "--password",
            help="Not required with a wired connection." +
                 "Optionally, set the PYNETGEAR_PASSWORD environment variable")
    router_args.add_argument(
            "--url", help="Overrides host:port and ssl with url to router")
    router_args.add_argument("--no-ssl",
                             dest="ssl", default=True,
                             action="store_false",
                             help="Connect with https")

    subparsers = parser.add_subparsers(
            description="Runs subcommand against the specified router",
            dest="subcommand")

    block_parser = subparsers.add_parser(
            "block_device",
            help="Blocks a device from connecting by mac address")
    block_parser.add_argument("--mac-addr")

    allow_parser = subparsers.add_parser(
            "allow_device",
            help="Allows a device with the mac address to connect")
    allow_parser.add_argument("--mac-addr")

    subparsers.add_parser("login", help="Attempts to login to router.")

    attached_devices = subparsers.add_parser("attached_devices", help="Outputs all attached devices")
    attached_devices.add_argument(
            "-v", "--verbose",
            action="store_true",
            default=False,
            help="Choose between verbose and slower or terse and fast.")

    subparsers.add_parser("traffic_meter", help="Output router's traffic meter data")

    return parser