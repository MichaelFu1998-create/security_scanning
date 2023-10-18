def get_key(key_name,
            value_name,
            jsonify,
            no_decrypt,
            stash,
            passphrase,
            backend):
    """Retrieve a key from the stash

    \b
    `KEY_NAME` is the name of the key to retrieve
    `VALUE_NAME` is a single value to retrieve e.g. if the value
     of the key `test` is `a=b,b=c`, `ghost get test a`a will return
     `b`
    """
    if value_name and no_decrypt:
        sys.exit('VALUE_NAME cannot be used in conjuction with --no-decrypt')

    stash = _get_stash(backend, stash, passphrase, quiet=jsonify or value_name)

    try:
        key = stash.get(key_name=key_name, decrypt=not no_decrypt)
    except GhostError as ex:
        sys.exit(ex)

    if not key:
        sys.exit('Key `{0}` not found'.format(key_name))
    if value_name:
        key = key['value'].get(value_name)
        if not key:
            sys.exit(
                'Value name `{0}` could not be found under key `{1}`'.format(
                    value_name, key_name))

    if jsonify or value_name:
        click.echo(
            json.dumps(key, indent=4, sort_keys=False).strip('"'),
            nl=True)
    else:
        click.echo('Retrieving key...')
        click.echo('\n' + _prettify_dict(key))