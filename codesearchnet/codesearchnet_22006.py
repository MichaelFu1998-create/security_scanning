def get_sites(self):
        """
        Returns a list of sites.

        http://dev.wheniwork.com/#listing-sites
        """
        url = "/2/sites"

        data = self._get_resource(url)
        sites = []
        for entry in data['sites']:
            sites.append(self.site_from_json(entry))

        return sites