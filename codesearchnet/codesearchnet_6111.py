def _init_config():
    """Setup configuration dictionary from default, command line and configuration file."""
    cli_opts, parser = _init_command_line_options()
    cli_verbose = cli_opts["verbose"]

    # Set config defaults
    config = copy.deepcopy(DEFAULT_CONFIG)

    # Configuration file overrides defaults
    config_file = cli_opts.get("config_file")
    if config_file:
        file_opts = _read_config_file(config_file, cli_verbose)
        util.deep_update(config, file_opts)
        if cli_verbose != DEFAULT_VERBOSE and "verbose" in file_opts:
            if cli_verbose >= 2:
                print(
                    "Config file defines 'verbose: {}' but is overridden by command line: {}.".format(
                        file_opts["verbose"], cli_verbose
                    )
                )
            config["verbose"] = cli_verbose
    else:
        if cli_verbose >= 2:
            print("Running without configuration file.")

    # Command line overrides file
    if cli_opts.get("port"):
        config["port"] = cli_opts.get("port")
    if cli_opts.get("host"):
        config["host"] = cli_opts.get("host")
    if cli_opts.get("profile") is not None:
        config["profile"] = True
    if cli_opts.get("server") is not None:
        config["server"] = cli_opts.get("server")
    if cli_opts.get("ssl_adapter") is not None:
        config["ssl_adapter"] = cli_opts.get("ssl_adapter")

    # Command line overrides file only if -v or -q where passed:
    if cli_opts.get("verbose") != DEFAULT_VERBOSE:
        config["verbose"] = cli_opts.get("verbose")

    if cli_opts.get("root_path"):
        root_path = os.path.abspath(cli_opts.get("root_path"))
        config["provider_mapping"]["/"] = FilesystemProvider(root_path)

    if config["verbose"] >= 5:
        # TODO: remove passwords from user_mapping
        # config_cleaned = copy.deepcopy(config)
        print("Configuration({}):\n{}".format(cli_opts["config_file"], pformat(config)))

    if not config["provider_mapping"]:
        parser.error("No DAV provider defined.")

    # Quick-configuration of DomainController
    auth = cli_opts.get("auth")
    auth_conf = config.get("http_authenticator", {})
    if auth and auth_conf.get("domain_controller"):
        parser.error(
            "--auth option can only be used when no domain_controller is configured"
        )

    if auth == "anonymous":
        if config["simple_dc"]["user_mapping"]:
            parser.error(
                "--auth=anonymous can only be used when no user_mapping is configured"
            )
        auth_conf.update(
            {
                "domain_controller": "wsgidav.dc.simple_dc.SimpleDomainController",
                "accept_basic": True,
                "accept_digest": True,
                "default_to_digest": True,
            }
        )
        config["simple_dc"]["user_mapping"] = {"*": True}
    elif auth == "nt":
        if config.get("nt_dc"):
            parser.error(
                "--auth=nt can only be used when no nt_dc settings are configured"
            )
        auth_conf.update(
            {
                "domain_controller": "wsgidav.dc.nt_dc.NTDomainController",
                "accept_basic": True,
                "accept_digest": False,
                "default_to_digest": False,
            }
        )
        config["nt_dc"] = {}
    elif auth == "pam-login":
        if config.get("pam_dc"):
            parser.error(
                "--auth=pam-login can only be used when no pam_dc settings are configured"
            )
        auth_conf.update(
            {
                "domain_controller": "wsgidav.dc.pam_dc.PAMDomainController",
                "accept_basic": True,
                "accept_digest": False,
                "default_to_digest": False,
            }
        )
        config["pam_dc"] = {"service": "login"}
    # print(config)

    if cli_opts.get("reload"):
        print("Installing paste.reloader.", file=sys.stderr)
        from paste import reloader  # @UnresolvedImport

        reloader.install()
        if config_file:
            # Add config file changes
            reloader.watch_file(config_file)
        # import pydevd
        # pydevd.settrace()

    return config