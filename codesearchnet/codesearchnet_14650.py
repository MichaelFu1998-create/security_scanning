def delete_key(key_name, stash, passphrase, backend):
    """Delete a key from the stash

    `KEY_NAME` is the name of the key to delete
    You can provide that multiple times to delete multiple keys at once
    """
    stash = _get_stash(backend, stash, passphrase)

    for key in key_name:
        try:
            click.echo('Deleting key {0}...'.format(key))
            stash.delete(key_name=key)
        except GhostError as ex:
            sys.exit(ex)
    click.echo('Keys deleted successfully')