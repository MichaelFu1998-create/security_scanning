def set_site_specifics(self, site):
        """
        Loads settings for the target site.
        """
        r = self.local_renderer
        site_data = self.genv.sites[site].copy()
        r.env.site = site
        if self.verbose:
            print('set_site_specifics.data:')
            pprint(site_data, indent=4)

        # Remove local namespace settings from the global namespace
        # by converting <satchel_name>_<variable_name> to <variable_name>.
        local_ns = {}
        for k, v in list(site_data.items()):
            if k.startswith(self.name + '_'):
                _k = k[len(self.name + '_'):]
                local_ns[_k] = v
                del site_data[k]

        r.env.update(local_ns)
        r.env.update(site_data)