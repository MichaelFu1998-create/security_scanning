def unlock_key(key_name,
               stash,
               passphrase,
               backend):
    """Unlock a key to allow it to be modified, deleted or purged

    `KEY_NAME` is the name of the key to unlock
    """
    stash = _get_stash(backend, stash, passphrase)

    try:
        click.echo('Unlocking key...')
        stash.unlock(key_name=key_name)
        click.echo('Key unlocked successfully')
    except GhostError as ex:
        sys.exit(ex)