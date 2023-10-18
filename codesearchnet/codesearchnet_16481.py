def check_cli_version():
    """Check if the current cli version satisfies the server requirements"""
    if not CliConfigManager.should_check():
        return

    server_version = get_server_version()
    current_version = get_current_version()
    CliConfigManager.reset(current_version=current_version,
                           min_version=server_version.min_version)

    if LooseVersion(current_version) < LooseVersion(server_version.min_version):
        click.echo("""Your version of CLI ({}) is no longer compatible with server.""".format(
            current_version))
        if click.confirm("Do you want to upgrade to "
                         "version {} now?".format(server_version.latest_version)):
            pip_upgrade()
            sys.exit(0)
        else:
            clint.textui.puts("Your can manually run:")
            with clint.textui.indent(4):
                clint.textui.puts("pip install -U polyaxon-cli")
            clint.textui.puts(
                "to upgrade to the latest version `{}`".format(server_version.latest_version))

            sys.exit(0)
    elif LooseVersion(current_version) < LooseVersion(server_version.latest_version):
        clint.textui.puts("New version of CLI ({}) is now available. To upgrade run:".format(
            server_version.latest_version
        ))
        with clint.textui.indent(4):
            clint.textui.puts("pip install -U polyaxon-cli")
    elif LooseVersion(current_version) > LooseVersion(server_version.latest_version):
        clint.textui.puts("You version of CLI ({}) is ahead of the latest version "
                          "supported by Polyaxon Platform ({}) on your cluster, "
                          "and might be incompatible.".format(current_version,
                                                              server_version.latest_version))