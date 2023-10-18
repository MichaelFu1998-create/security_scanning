def deploy_code(self):
        """
        Generates a rsync of all deployable code.
        """

        assert self.genv.SITE, 'Site unspecified.'
        assert self.genv.ROLE, 'Role unspecified.'

        r = self.local_renderer

        if self.env.exclusions:
            r.env.exclusions_str = ' '.join(
                "--exclude='%s'" % _ for _ in self.env.exclusions)

        r.local(r.env.rsync_command)
        r.sudo('chown -R {rsync_chown_user}:{rsync_chown_group} {rsync_dst_dir}')