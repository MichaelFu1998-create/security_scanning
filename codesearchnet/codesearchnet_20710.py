def get_config_value(name, fallback=None):
    """Gets a config by name.

    In the case where the config name is not found, will use fallback value."""

    cli_config = CLIConfig(SF_CLI_CONFIG_DIR, SF_CLI_ENV_VAR_PREFIX)

    return cli_config.get('servicefabric', name, fallback)