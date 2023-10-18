def config(key=None, value=None, scope='user', global_=False, unset=False):
    """Read or write tower-cli configuration.

    `tower config` saves the given setting to the appropriate Tower CLI;
    either the user's ~/.tower_cli.cfg file, or the /etc/tower/tower_cli.cfg
    file if --global is used.

    Writing to /etc/tower/tower_cli.cfg is likely to require heightened
    permissions (in other words, sudo).
    """
    # If the old-style `global_` option is set, issue a deprecation notice.
    if global_:
        scope = 'global'
        warnings.warn('The `--global` option is deprecated and will be '
                      'removed. Use `--scope=global` to get the same effect.',
                      DeprecationWarning)

    # If no key was provided, print out the current configuration
    # in play.
    if not key:
        seen = set()
        parser_desc = {
            'runtime': 'Runtime options.',
            'environment': 'Options from environment variables.',
            'local': 'Local options (set with `tower-cli config '
                     '--scope=local`; stored in .tower_cli.cfg of this '
                     'directory or a parent)',
            'user': 'User options (set with `tower-cli config`; stored in '
                    '~/.tower_cli.cfg).',
            'global': 'Global options (set with `tower-cli config '
                      '--scope=global`, stored in /etc/tower/tower_cli.cfg).',
            'defaults': 'Defaults.',
        }

        # Iterate over each parser (English: location we can get settings from)
        # and print any settings that we haven't already seen.
        #
        # We iterate over settings from highest precedence to lowest, so any
        # seen settings are overridden by the version we iterated over already.
        click.echo('')
        for name, parser in zip(settings._parser_names, settings._parsers):
            # Determine if we're going to see any options in this
            # parser that get echoed.
            will_echo = False
            for option in parser.options('general'):
                if option in seen:
                    continue
                will_echo = True

            # Print a segment header
            if will_echo:
                secho('# %s' % parser_desc[name], fg='green', bold=True)

            # Iterate over each option in the parser and, if we haven't
            # already seen an option at higher precedence, print it.
            for option in parser.options('general'):
                if option in seen:
                    continue
                _echo_setting(option)
                seen.add(option)

            # Print a nice newline, for formatting.
            if will_echo:
                click.echo('')
        return

    # Sanity check: Is this a valid configuration option? If it's not
    # a key we recognize, abort.
    if not hasattr(settings, key):
        raise exc.TowerCLIError('Invalid configuration option "%s".' % key)

    # Sanity check: The combination of a value and --unset makes no
    # sense.
    if value and unset:
        raise exc.UsageError('Cannot provide both a value and --unset.')

    # If a key was provided but no value was provided, then just
    # print the current value for that key.
    if key and not value and not unset:
        _echo_setting(key)
        return

    # Okay, so we're *writing* a key. Let's do this.
    # First, we need the appropriate file.
    filename = os.path.expanduser('~/.tower_cli.cfg')
    if scope == 'global':
        if not os.path.isdir('/etc/tower/'):
            raise exc.TowerCLIError('/etc/tower/ does not exist, and this '
                                    'command cowardly declines to create it.')
        filename = '/etc/tower/tower_cli.cfg'
    elif scope == 'local':
        filename = '.tower_cli.cfg'

    # Read in the appropriate config file, write this value, and save
    # the result back to the file.
    parser = Parser()
    parser.add_section('general')
    parser.read(filename)
    if unset:
        parser.remove_option('general', key)
    else:
        parser.set('general', key, value)
    with open(filename, 'w') as config_file:
        parser.write(config_file)

    # Give rw permissions to user only fix for issue number 48
    try:
        os.chmod(filename, stat.S_IRUSR | stat.S_IWUSR)
    except Exception as e:
        warnings.warn(
            'Unable to set permissions on {0} - {1} '.format(filename, e),
            UserWarning
            )
    click.echo('Configuration updated successfully.')