def load_keys(key_file, origin_passphrase, stash, passphrase, backend):
    """Load all keys from an exported key file to the stash

    `KEY_FILE` is the exported stash file to load keys from
    """
    stash = _get_stash(backend, stash, passphrase)

    click.echo('Importing all keys from {0}...'.format(key_file))
    stash.load(origin_passphrase, key_file=key_file)
    click.echo('Import complete!')