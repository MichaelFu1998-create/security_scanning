def main():
    """Scan for devices and print results."""

    args = argparser().parse_args(sys.argv[1:])
    password = os.environ.get('PYNETGEAR_PASSWORD') or args.password

    netgear = Netgear(password, args.host, args.user, args.port, args.ssl, args.url, args.force_login_v2)

    results = run_subcommand(netgear, args)
    formatter = make_formatter(args.format)

    if results is None:
        print("Error communicating with the Netgear router")

    else:
        formatter(results)