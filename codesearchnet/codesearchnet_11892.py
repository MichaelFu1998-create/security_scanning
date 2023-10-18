def optimize_wsgi_processes(self):
        """
        Based on the number of sites per server and the number of resources on the server,
        calculates the optimal number of processes that should be allocated for each WSGI site.
        """
        r = self.local_renderer
        #r.env.wsgi_processes = 5
        r.env.wsgi_server_memory_gb = 8

        verbose = self.verbose

        all_sites = list(self.iter_sites(site=ALL, setter=self.set_site_specifics))