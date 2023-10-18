def run_on_all_sites(self, cmd, *args, **kwargs):
        """
        Like run(), but re-runs the command for each site in the current role.
        """
        r = self.local_renderer
        for _site, _data in iter_sites():
            r.env.SITE = _site
            with self.settings(warn_only=True):
                r.run('export SITE={SITE}; export ROLE={ROLE}; '+cmd)