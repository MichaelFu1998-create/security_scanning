def ssh(key_name, no_tunnel, stash, passphrase, backend):
    """Use an ssh type key to connect to a machine via ssh

    Note that trying to use a key of the wrong type (e.g. `secret`)
    will result in an error.

    `KEY_NAME` is the key to use.

    For additional information on the different configuration options
    for an ssh type key, see the repo's readme.
    """
    # TODO: find_executable or raise
    def execute(command):
        try:
            click.echo('Executing: {0}'.format(' '.join(command)))
            subprocess.check_call(' '.join(command), shell=True)
        except subprocess.CalledProcessError:
            sys.exit(1)

    stash = _get_stash(backend, stash, passphrase)
    key = stash.get(key_name)

    if key:
        _assert_is_ssh_type_key(key)
    else:
        sys.exit('Key `{0}` not found'.format(key_name))

    conn_info = key['value']
    ssh_key_path = conn_info.get('ssh_key_path')
    ssh_key = conn_info.get('ssh_key')
    proxy_key_path = conn_info.get('proxy_key_path')
    proxy_key = conn_info.get('proxy_key')

    id_file = _write_tmp(ssh_key) if ssh_key else ssh_key_path
    conn_info['ssh_key_path'] = id_file

    if conn_info.get('proxy'):
        proxy_id_file = _write_tmp(proxy_key) if proxy_key else proxy_key_path
        conn_info['proxy_key_path'] = proxy_id_file

    ssh_command = _build_ssh_command(conn_info, no_tunnel)
    try:
        execute(ssh_command)
    finally:
        # If they're not equal, that means we've created a temp one which
        # should be deleted, else, it's a path to an existing key file.
        if id_file != ssh_key_path:
            click.echo('Removing temp ssh key file: {0}...'.format(id_file))
            os.remove(id_file)
        if conn_info.get('proxy') and proxy_id_file != proxy_key_path:
            click.echo('Removing temp proxy key file: {0}...'.format(
                proxy_id_file))
            os.remove(proxy_id_file)