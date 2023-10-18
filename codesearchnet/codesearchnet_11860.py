def manage_all(self, *args, **kwargs):
        """
        Runs manage() across all unique site default databases.
        """
        for site, site_data in self.iter_unique_databases(site='all'):
            if self.verbose:
                print('-'*80, file=sys.stderr)
                print('site:', site, file=sys.stderr)
            if self.env.available_sites_by_host:
                hostname = self.current_hostname
                sites_on_host = self.env.available_sites_by_host.get(hostname, [])
                if sites_on_host and site not in sites_on_host:
                    self.vprint('skipping site:', site, sites_on_host, file=sys.stderr)
                    continue
            self.manage(*args, **kwargs)