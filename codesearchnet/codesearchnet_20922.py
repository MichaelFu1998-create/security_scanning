def _url(self, url=None, parameters=None):
        """ Build destination URL.

        Kwargs:
            url (str): Destination URL
            parameters (dict): Additional GET parameters to append to the URL

        Returns:
            str. URL 
        """

        uri = url or self._settings["url"]
        if url and self._settings["base_url"]:
            uri = "%s/%s" % (self._settings["base_url"], url)
        uri += ".json"
        if parameters:
            uri += "?%s" % urllib.urlencode(parameters)
        return uri