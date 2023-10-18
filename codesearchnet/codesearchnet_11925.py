def create_supervisor_services(self, site):
        """
        This is called for each site to render a Celery config file.
        """

        self.vprint('create_supervisor_services:', site)

        self.set_site_specifics(site=site)

        r = self.local_renderer
        if self.verbose:
            print('r.env:')
            pprint(r.env, indent=4)

        self.vprint('r.env.has_worker:', r.env.has_worker)
        if not r.env.has_worker:
            self.vprint('skipping: no celery worker')
            return

        if self.name.lower() not in self.genv.services:
            self.vprint('skipping: celery not enabled')
            return

        hostname = self.current_hostname
        target_sites = self.genv.available_sites_by_host.get(hostname, None)
        if target_sites and site not in target_sites:
            self.vprint('skipping: site not supported on this server')
            return

        self.render_paths()

        conf_name = 'celery_%s.conf' % site
        ret = r.render_to_string('celery/celery_supervisor.template.conf')
        return conf_name, ret