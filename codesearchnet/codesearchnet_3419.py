def process_config_values(parser: argparse.ArgumentParser, args: argparse.Namespace):
    """
    Bring in provided config values to the args parser, and import entries to the config
    from all arguments that were actually passed on the command line

    :param parser: The arg parser
    :param args: The value that parser.parse_args returned
    """
    # First, load a local config file, if passed or look for one in pwd if it wasn't.
    load_overrides(args.config)

    # Get a list of defined config vals. If these are passed on the command line,
    # update them in their correct group, not in the cli group
    defined_vars = list(get_config_keys())

    command_line_args = vars(args)

    # Bring in the options keys into args
    config_cli_args = get_group('cli')

    # Place all command line args into the cli group (for saving in the workspace). If
    # the value is set on command line, then it takes precedence; otherwise we try to
    # read it from the config file's cli group.
    for k in command_line_args:
        default = parser.get_default(k)
        set_val = getattr(args, k)
        if default is not set_val:
            if k not in defined_vars:
                config_cli_args.update(k, value=set_val)
            else:
                # Update a var's native group
                group_name, key = k.split('.')
                group = get_group(group_name)
                setattr(group, key, set_val)
        else:
            if k in config_cli_args:
                setattr(args, k, getattr(config_cli_args, k))