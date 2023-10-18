def cli(context, verbose):
    """ Polyaxon CLI tool to:

        * Parse, Validate, and Check Polyaxonfiles.

        * Interact with Polyaxon server.

        * Run and Monitor experiments.

    Check the help available for each command listed below.
    """
    configure_logger(verbose or GlobalConfigManager.get_value('verbose'))
    non_check_cmds = ['config', 'version', 'login', 'logout', 'deploy', 'admin', 'teardown']
    if context.invoked_subcommand not in non_check_cmds:
        check_cli_version()