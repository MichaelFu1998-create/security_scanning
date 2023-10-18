def base_url(self):
        """A base_url that will be used to construct the final
        URL we're going to query against.

        :returns: A URL of the form: ``proto://host:port``.
        :rtype: :obj:`string`
        """
        return '{proto}://{host}:{port}{url_path}'.format(
            proto=self.protocol,
            host=self.host,
            port=self.port,
            url_path=self.url_path,
        )