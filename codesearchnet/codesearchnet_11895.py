def sync_media(self, sync_set=None, clean=0, iter_local_paths=0):
        """
        Uploads select media to an Apache accessible directory.
        """

        # Ensure a site is selected.
        self.genv.SITE = self.genv.SITE or self.genv.default_site

        r = self.local_renderer

        clean = int(clean)
        self.vprint('Getting site data for %s...' % self.genv.SITE)

        self.set_site_specifics(self.genv.SITE)

        sync_sets = r.env.sync_sets
        if sync_set:
            sync_sets = [sync_set]

        ret_paths = []
        for _sync_set in sync_sets:
            for paths in r.env.sync_sets[_sync_set]:
                r.env.sync_local_path = os.path.abspath(paths['local_path'] % self.genv)
                if paths['local_path'].endswith('/') and not r.env.sync_local_path.endswith('/'):
                    r.env.sync_local_path += '/'

                if iter_local_paths:
                    ret_paths.append(r.env.sync_local_path)
                    continue

                r.env.sync_remote_path = paths['remote_path'] % self.genv

                if clean:
                    r.sudo('rm -Rf {apache_sync_remote_path}')

                print('Syncing %s to %s...' % (r.env.sync_local_path, r.env.sync_remote_path))

                r.env.tmp_chmod = paths.get('chmod', r.env.chmod)
                r.sudo('mkdir -p {apache_sync_remote_path}')
                r.sudo('chmod -R {apache_tmp_chmod} {apache_sync_remote_path}')
                r.local('rsync -rvz --progress --recursive --no-p --no-g '
                    '--rsh "ssh -o StrictHostKeyChecking=no -i {key_filename}" {apache_sync_local_path} {user}@{host_string}:{apache_sync_remote_path}')
                r.sudo('chown -R {apache_web_user}:{apache_web_group} {apache_sync_remote_path}')

        if iter_local_paths:
            return ret_paths