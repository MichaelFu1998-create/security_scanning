def with_global_options(method):
    """Apply the global options that we desire on every method within
    tower-cli to the given click command.
    """
    # Create global options for the Tower host, username, and password.
    #
    # These are runtime options that will override the configuration file
    # settings.
    method = click.option(
        '-h', '--tower-host',
        help='The location of the Ansible Tower host. '
             'HTTPS is assumed as the protocol unless "http://" is explicitly '
             'provided. This will take precedence over a host provided to '
             '`tower config`, if any.',
        required=False, callback=_apply_runtime_setting,
        is_eager=True,
        expose_value=False
    )(method)
    method = click.option(
        '-t', '--tower-oauth-token',
        help='OAuth2 token to use to authenticate to Ansible Tower. '
             'This will take precedence over a token provided to '
             '`tower config`, if any.',
        required=False, callback=_apply_runtime_setting,
        is_eager=True,
        expose_value=False
    )(method)
    method = click.option(
        '-u', '--tower-username',
        help='Username to use to authenticate to Ansible Tower. '
             'This will take precedence over a username provided to '
             '`tower config`, if any.',
        required=False, callback=_apply_runtime_setting,
        is_eager=True,
        expose_value=False
    )(method)
    method = click.option(
        '-p', '--tower-password',
        help='Password to use to authenticate to Ansible Tower. '
             'This will take precedence over a password provided to '
             '`tower config`, if any. If value is ASK you will be '
             'prompted for the password',
        required=False, callback=_apply_runtime_setting,
        is_eager=True,
        expose_value=False
    )(method)

    # Create a global verbose/debug option.
    method = click.option(
        '-f', '--format',
        help='Output format. The "human" format is intended for humans '
             'reading output on the CLI; the "json" and "yaml" formats '
             'provide more data, and "id" echos the object id only.',
        type=click.Choice(['human', 'json', 'yaml', 'id']),
        required=False, callback=_apply_runtime_setting,
        is_eager=True,
        expose_value=False
    )(method)
    method = click.option(
        '-v', '--verbose',
        default=None,
        help='Show information about requests being made.',
        is_flag=True,
        required=False, callback=_apply_runtime_setting,
        is_eager=True,
        expose_value=False
    )(method)
    method = click.option(
        '--description-on',
        default=None,
        help='Show description in human-formatted output.',
        is_flag=True,
        required=False, callback=_apply_runtime_setting,
        is_eager=True,
        expose_value=False
    )(method)

    # Create a global SSL warning option.
    method = click.option(
        '--insecure',
        default=None,
        help='Turn off insecure connection warnings. Set config verify_ssl '
             'to make this permanent.',
        is_flag=True,
        required=False, callback=_apply_runtime_setting,
        is_eager=True,
        expose_value=False
    )(method)

    # Create a custom certificate specification option.
    method = click.option(
        '--certificate',
        default=None,
        help='Path to a custom certificate file that will be used throughout'
             ' the command. Overwritten by --insecure flag if set.',
        required=False, callback=_apply_runtime_setting,
        is_eager=True,
        expose_value=False
    )(method)

    method = click.option(
        '--use-token',
        default=None,
        help='Turn on Tower\'s token-based authentication. No longer supported '
             'in Tower 3.3 and above.',
        is_flag=True,
        required=False, callback=_apply_runtime_setting,
        is_eager=True,
        expose_value=False
    )(method)
    # Manage the runtime settings context
    method = runtime_context_manager(method)

    # Okay, we're done adding options; return the method.
    return method