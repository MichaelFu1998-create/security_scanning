def get(keys):
    """Get the global config values by keys.

    Example:

    \b
    ```bash
    $ polyaxon config get host http_port
    ```
    """
    _config = GlobalConfigManager.get_config_or_default()

    if not keys:
        return

    print_values = {}
    for key in keys:
        if hasattr(_config, key):
            print_values[key] = getattr(_config, key)
        else:
            click.echo('Key `{}` is not recognised.'.format(key))

    dict_tabulate(print_values, )