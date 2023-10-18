def init_stash(stash_path, passphrase, passphrase_size, backend):
    r"""Init a stash

    `STASH_PATH` is the path to the storage endpoint. If this isn't supplied,
    a default path will be used. In the path, you can specify a name
    for the stash (which, if omitted, will default to `ghost`) like so:
    `ghost init http://10.10.1.1:8500;stash1`.

    After initializing a stash, don't forget you can set environment
    variables for both your stash's path and its passphrase.
    On Linux/OSx you can run:

    export GHOST_STASH_PATH='http://10.10.1.1:8500;stash1'

    export GHOST_PASSPHRASE=$(cat passphrase.ghost)

    export GHOST_BACKEND='tinydb'
    """
    stash_path = stash_path or STORAGE_DEFAULT_PATH_MAPPING[backend]
    click.echo('Stash: {0} at {1}'.format(backend, stash_path))
    storage = STORAGE_MAPPING[backend](**_parse_path_string(stash_path))

    try:
        click.echo('Initializing stash...')
        if os.path.isfile(PASSPHRASE_FILENAME):
            raise GhostError(
                '{0} already exists. Overwriting might prevent you '
                'from accessing the stash it was generated for. '
                'Please make sure to save and remove the file before '
                'initializing another stash.'.format(PASSPHRASE_FILENAME))

        stash = Stash(
            storage,
            passphrase=passphrase,
            passphrase_size=passphrase_size)
        passphrase = stash.init()

        if not passphrase:
            click.echo('Stash already initialized.')
            sys.exit(0)

        _write_passphrase_file(passphrase)
    except GhostError as ex:
        sys.exit(ex)
    except (OSError, IOError) as ex:
        click.echo("Seems like we've run into a problem.")
        file_path = _parse_path_string(stash_path)['db_path']
        click.echo(
            'Removing stale stash and passphrase: {0}. Note that any '
            'directories created are not removed for safety reasons and you '
            'might want to remove them manually.'.format(file_path))
        if os.path.isfile(file_path):
            os.remove(file_path)
        sys.exit(ex)

    click.echo('Initialized stash at: {0}'.format(stash_path))
    click.echo(
        'Your passphrase can be found under the `{0}` file in the '
        'current directory.'.format(PASSPHRASE_FILENAME))
    click.echo(
        'Make sure you save your passphrase somewhere safe. '
        'If lost, you will lose access to your stash.')