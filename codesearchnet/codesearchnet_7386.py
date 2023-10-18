def _retrieve_data(self, request=None):
        """
        Retrieve Zotero items via the API
        Combine endpoint and request to access the specific resource
        Returns a JSON document
        """
        full_url = "%s%s" % (self.endpoint, request)
        # The API doesn't return this any more, so we have to cheat
        self.self_link = request
        self.request = requests.get(url=full_url, headers=self.default_headers())
        self.request.encoding = "utf-8"
        try:
            self.request.raise_for_status()
        except requests.exceptions.HTTPError:
            error_handler(self.request)
        return self.request