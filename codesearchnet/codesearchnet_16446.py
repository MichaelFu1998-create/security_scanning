def login(token, username, password):
    """Login to Polyaxon."""
    auth_client = PolyaxonClient().auth
    if username:
        # Use username / password login
        if not password:
            password = click.prompt('Please enter your password', type=str, hide_input=True)
            password = password.strip()
            if not password:
                logger.info('You entered an empty string. '
                            'Please make sure you enter your password correctly.')
                sys.exit(1)

        credentials = CredentialsConfig(username=username, password=password)
        try:
            access_code = auth_client.login(credentials=credentials)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not login.')
            Printer.print_error('Error Message `{}`.'.format(e))
            sys.exit(1)

        if not access_code:
            Printer.print_error("Failed to login")
            return
    else:
        if not token:
            token_url = "{}/app/token".format(auth_client.config.http_host)
            click.confirm('Authentication token page will now open in your browser. Continue?',
                          abort=True, default=True)

            click.launch(token_url)
            logger.info("Please copy and paste the authentication token.")
            token = click.prompt('This is an invisible field. Paste token and press ENTER',
                                 type=str, hide_input=True)

        if not token:
            logger.info("Empty token received. "
                        "Make sure your shell is handling the token appropriately.")
            logger.info("See docs for help: http://docs.polyaxon.com/polyaxon_cli/commands/auth")
            return

        access_code = token.strip(" ")

    # Set user
    try:
        AuthConfigManager.purge()
        user = PolyaxonClient().auth.get_user(token=access_code)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not load user info.')
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)
    access_token = AccessTokenConfig(username=user.username, token=access_code)
    AuthConfigManager.set_config(access_token)
    Printer.print_success("Login successful")

    # Reset current cli
    server_version = get_server_version()
    current_version = get_current_version()
    log_handler = get_log_handler()
    CliConfigManager.reset(check_count=0,
                           current_version=current_version,
                           min_version=server_version.min_version,
                           log_handler=log_handler)