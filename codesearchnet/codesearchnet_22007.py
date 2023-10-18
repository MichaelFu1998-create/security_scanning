def create_site(self, params={}):
        """
        Creates a site

        http://dev.wheniwork.com/#create-update-site
        """
        url = "/2/sites/"
        body = params

        data = self._post_resource(url, body)
        return self.site_from_json(data["site"])