def sync(self, sync_set, force=0, site=None, role=None):
        """
        Uploads media to an Amazon S3 bucket using s3sync.

        Requires s3cmd. Install with:

            pip install s3cmd

        """
        from burlap.dj import dj
        force = int(force)

        r = self.local_renderer

        r.env.sync_force_flag = ' --force ' if force else ''

        _settings = dj.get_settings(site=site, role=role)
        assert _settings, 'Unable to import settings.'
        for k in _settings.__dict__.iterkeys():
            if k.startswith('AWS_'):
                r.genv[k] = _settings.__dict__[k]

        site_data = r.genv.sites[r.genv.SITE]
        r.env.update(site_data)

        r.env.virtualenv_bin_dir = os.path.split(sys.executable)[0]

        rets = []
        for paths in r.env.sync_sets[sync_set]:
            is_local = paths.get('is_local', True)
            local_path = paths['local_path'] % r.genv
            remote_path = paths['remote_path']
            remote_path = remote_path.replace(':/', '/')
            if not remote_path.startswith('s3://'):
                remote_path = 's3://' + remote_path
            local_path = local_path % r.genv

            if is_local:
                #local_or_dryrun('which s3sync')#, capture=True)
                r.env.local_path = os.path.abspath(local_path)
            else:
                #run('which s3sync')
                r.env.local_path = local_path

            if local_path.endswith('/') and not r.env.local_path.endswith('/'):
                r.env.local_path = r.env.local_path + '/'

            r.env.remote_path = remote_path % r.genv

            print('Syncing %s to %s...' % (r.env.local_path, r.env.remote_path))

            # Superior Python version.
            if force:
                r.env.sync_cmd = 'put'
            else:
                r.env.sync_cmd = 'sync'
            r.local(
                'export AWS_ACCESS_KEY_ID={aws_access_key_id}; '\
                'export AWS_SECRET_ACCESS_KEY={aws_secret_access_key}; '\
                '{s3cmd_path} {sync_cmd} --progress --acl-public --guess-mime-type --no-mime-magic '\
                '--delete-removed --cf-invalidate --recursive {sync_force_flag} '\
                '{local_path} {remote_path}')