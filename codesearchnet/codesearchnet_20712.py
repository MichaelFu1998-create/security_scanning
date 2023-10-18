def set_config_value(name, value):
    """Set a config by name to a value."""

    cli_config = CLIConfig(SF_CLI_CONFIG_DIR, SF_CLI_ENV_VAR_PREFIX)
    cli_config.set_value('servicefabric', name, value)