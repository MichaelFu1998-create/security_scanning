def list_keys(key_name,
              max_suggestions,
              cutoff,
              jsonify,
              locked,
              key_type,
              stash,
              passphrase,
              backend):
    """List all keys in the stash

    If `KEY_NAME` is provided, will look for keys containing `KEY_NAME`.
    If `KEY_NAME` starts with `~`, close matches will be provided according
    to `max_suggestions` and `cutoff`.
    """
    stash = _get_stash(backend, stash, passphrase, quiet=jsonify)

    try:
        keys = stash.list(
            key_name=key_name,
            max_suggestions=max_suggestions,
            cutoff=cutoff,
            locked_only=locked,
            key_type=key_type)
    except GhostError as ex:
        sys.exit(ex)
    if jsonify:
        click.echo(json.dumps(keys, indent=4, sort_keys=True))
    elif not keys:
        click.echo('The stash is empty. Go on, put some keys in there...')
    else:
        click.echo('Listing all keys...')
        click.echo(_prettify_list(keys))