def set(verbose,  # pylint:disable=redefined-builtin
        host,
        http_port,
        ws_port,
        use_https,
        verify_ssl):
    """Set the global config values.

    Example:

    \b
    ```bash
    $ polyaxon config set --hots=localhost http_port=80
    ```
    """
    _config = GlobalConfigManager.get_config_or_default()

    if verbose is not None:
        _config.verbose = verbose

    if host is not None:
        _config.host = host

    if http_port is not None:
        _config.http_port = http_port

    if ws_port is not None:
        _config.ws_port = ws_port

    if use_https is not None:
        _config.use_https = use_https

    if verify_ssl is False:
        _config.verify_ssl = verify_ssl

    GlobalConfigManager.set_config(_config)
    Printer.print_success('Config was updated.')
    # Reset cli config
    CliConfigManager.purge()