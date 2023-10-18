def _make_url(self, slug):
        """
        Ensures that the request url is valid.
        Sometimes we have URLs that the server gives that are preformatted,
        sometimes we need to form our own.
        """
        if slug.startswith("http"):
            return slug
        return "{0}{1}".format(self.server_url, slug)