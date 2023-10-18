def get_config_bool(name):
    """Checks if a config value is set to a valid bool value."""

    cli_config = CLIConfig(SF_CLI_CONFIG_DIR, SF_CLI_ENV_VAR_PREFIX)
    return cli_config.getboolean('servicefabric', name, False)