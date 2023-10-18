def default_headers(self):
        """
        It's always OK to include these headers
        """
        _headers = {
            "User-Agent": "Pyzotero/%s" % __version__,
            "Zotero-API-Version": "%s" % __api_version__,
        }
        if self.api_key:
            _headers["Authorization"] = "Bearer %s" % self.api_key
        return _headers