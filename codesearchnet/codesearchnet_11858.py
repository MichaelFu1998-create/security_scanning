def loaddata(self, path, site=None):
        """
        Runs the Dango loaddata management command.

        By default, runs on only the current site.

        Pass site=all to run on all sites.
        """
        site = site or self.genv.SITE
        r = self.local_renderer
        r.env._loaddata_path = path
        for _site, site_data in self.iter_sites(site=site, no_secure=True):
            try:
                self.set_db(site=_site)
                r.env.SITE = _site
                r.sudo('export SITE={SITE}; export ROLE={ROLE}; '
                    'cd {project_dir}; '
                    '{manage_cmd} loaddata {_loaddata_path}')
            except KeyError:
                pass