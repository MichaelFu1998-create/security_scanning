def upload_pgp_keys():
    """ upload and/or update the PGP keys for editors, import them into PGP"""
    get_vars()
    upload_target = '/tmp/pgp_pubkeys.tmp'
    with fab.settings(fab.hide('running')):
        fab.run('rm -rf %s' % upload_target)
        fab.run('mkdir %s' % upload_target)
        local_key_path = path.join(fab.env['config_base'], fab.env.instance.config['local_pgpkey_path'])
        remote_key_path = '/var/briefkasten/pgp_pubkeys/'.format(**AV)
        rsync('-av', local_key_path, '{host_string}:%s' % upload_target)
        fab.run('chown -R %s %s' % (AV['appuser'], remote_key_path))
        fab.run('chmod 700 %s' % remote_key_path)
        with fab.shell_env(GNUPGHOME=remote_key_path):
            fab.sudo('''gpg --import %s/*.*''' % upload_target,
                user=AV['appuser'], shell_escape=False)
        fab.run('rm -rf %s' % upload_target)