def read(args):
    """Reading the configure file and adds non-existing attributes to 'args'"""

    if args.config_file is None or not isfile(args.config_file):
        return

    logging.info("Reading configure file: %s"%args.config_file)

    config = cparser.ConfigParser()
    config.read(args.config_file)
    if not config.has_section('lrcloud'):
        raise RuntimeError("Configure file has no [lrcloud] section!")

    for (name, value) in config.items('lrcloud'):
        if value == "True":
            value = True
        elif value == "False":
            value = False
        if getattr(args, name) is None:
            setattr(args, name, value)