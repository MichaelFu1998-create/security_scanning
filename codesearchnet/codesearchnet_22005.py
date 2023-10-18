def get_site(self, site_id):
        """
        Returns site data.

        http://dev.wheniwork.com/#get-existing-site
        """
        url = "/2/sites/%s" % site_id

        return self.site_from_json(self._get_resource(url)["site"])