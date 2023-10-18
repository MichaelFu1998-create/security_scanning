def put_key(key_name,
            value,
            description,
            meta,
            modify,
            add,
            lock,
            key_type,
            stash,
            passphrase,
            backend):
    """Insert a key to the stash

    `KEY_NAME` is the name of the key to insert

    `VALUE` is a key=value argument which can be provided multiple times.
    it is the encrypted value of your key
    """
    stash = _get_stash(backend, stash, passphrase)

    try:
        click.echo('Stashing {0} key...'.format(key_type))
        stash.put(
            name=key_name,
            value=_build_dict_from_key_value(value),
            modify=modify,
            metadata=_build_dict_from_key_value(meta),
            description=description,
            lock=lock,
            key_type=key_type,
            add=add)
        click.echo('Key stashed successfully')
    except GhostError as ex:
        sys.exit(ex)