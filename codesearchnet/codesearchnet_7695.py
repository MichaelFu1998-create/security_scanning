def run_subcommand(netgear, args):
    """Runs the subcommand configured in args on the netgear session"""

    subcommand = args.subcommand

    if subcommand == "block_device" or subcommand == "allow_device":
        return netgear.allow_block_device(args.mac_addr, BLOCK if subcommand == "block_device" else ALLOW)

    if subcommand == "attached_devices":
        if args.verbose:
            return netgear.get_attached_devices_2()
        else:
            return netgear.get_attached_devices()

    if subcommand == 'traffic_meter':
        return netgear.get_traffic_meter()

    if subcommand == 'login':
        return netgear.login()

    print("Unknown subcommand")