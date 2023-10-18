def last_modified_version(self, **kwargs):
        """ Get the last modified version
        """
        self.items(**kwargs)
        return int(self.request.headers.get("last-modified-version", 0))