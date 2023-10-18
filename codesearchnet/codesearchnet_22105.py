def write(args):
    """Writing the configure file with the attributes in 'args'"""

    logging.info("Writing configure file: %s"%args.config_file)
    if args.config_file is None:
        return

    #Let's add each attribute of 'args' to the configure file
    config = cparser.ConfigParser()
    config.add_section("lrcloud")
    for p in [x for x in dir(args) if not x.startswith("_")]:
        if p in IGNORE_ARGS:
            continue#We ignore some attributes
        value = getattr(args, p)
        if value is not None:
            config.set('lrcloud', p, str(value))

    with open(args.config_file, 'w') as f:
        config.write(f)