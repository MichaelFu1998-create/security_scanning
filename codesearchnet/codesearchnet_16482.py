def version(cli, platform):
    """Print the current version of the cli and platform."""
    version_client = PolyaxonClient().version
    cli = cli or not any([cli, platform])
    if cli:
        try:
            server_version = version_client.get_cli_version()
        except AuthorizationError:
            session_expired()
            sys.exit(1)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get cli version.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
        cli_version = get_version(PROJECT_CLI_NAME)
        Printer.print_header('Current cli version: {}.'.format(cli_version))
        Printer.print_header('Supported cli versions:')
        dict_tabulate(server_version.to_dict())

    if platform:
        try:
            platform_version = version_client.get_platform_version()
        except AuthorizationError:
            session_expired()
            sys.exit(1)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get platform version.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
        chart_version = version_client.get_chart_version()
        Printer.print_header('Current platform version: {}.'.format(chart_version.version))
        Printer.print_header('Supported platform versions:')
        dict_tabulate(platform_version.to_dict())