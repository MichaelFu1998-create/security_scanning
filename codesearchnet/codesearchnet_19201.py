def edit(self, config, etag):
        """Update template config for specified template name.

        .. __: https://api.go.cd/current/#edit-template-config

        Returns:
          Response: :class:`gocd.api.response.Response` object
        """

        data = self._json_encode(config)
        headers = self._default_headers()

        if etag is not None:
            headers["If-Match"] = etag

        return self._request(self.name,
                             ok_status=None,
                             data=data,
                             headers=headers,
                             method="PUT")