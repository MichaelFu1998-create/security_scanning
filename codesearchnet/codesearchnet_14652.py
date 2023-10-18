def purge_stash(force, stash, passphrase, backend):
    """Purge the stash from all of its keys
    """
    stash = _get_stash(backend, stash, passphrase)

    try:
        click.echo('Purging stash...')
        stash.purge(force)
        # Maybe we should verify that the list is empty
        # afterwards?
        click.echo('Purge complete!')
    except GhostError as ex:
        sys.exit(ex)