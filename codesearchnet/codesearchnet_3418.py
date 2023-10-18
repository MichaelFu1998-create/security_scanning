def add_config_vars_to_argparse(args):
    """
    Import all defined config vars into |args|, for parsing command line.
    :param args: A container for argparse vars
    :type args: argparse.ArgumentParser or argparse._ArgumentGroup
    :return:
    """
    global _groups
    for group_name, group in _groups.items():
        for key in group:
            obj = group._var_object(key)
            args.add_argument(f"--{group_name}.{key}", type=type(obj.default),
                              default=obj.default, help=obj.description)