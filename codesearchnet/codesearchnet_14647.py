def lock_key(key_name,
             stash,
             passphrase,
             backend):
    """Lock a key to prevent it from being deleted, purged or modified

    `KEY_NAME` is the name of the key to lock
    """
    stash = _get_stash(backend, stash, passphrase)

    try:
        click.echo('Locking key...')
        stash.lock(key_name=key_name)
        click.echo('Key locked successfully')
    except GhostError as ex:
        sys.exit(ex)