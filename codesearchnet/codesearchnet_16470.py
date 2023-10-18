def config(list):  # pylint:disable=redefined-builtin
    """Set and get the global configurations."""
    if list:
        _config = GlobalConfigManager.get_config_or_default()
        Printer.print_header('Current config:')
        dict_tabulate(_config.to_dict())