def delete(self):
        """Delete template config for specified template name.

        .. __: https://api.go.cd/current/#delete-a-template

        Returns:
          Response: :class:`gocd.api.response.Response` object
        """

        headers = self._default_headers()

        return self._request(self.name,
                             ok_status=None,
                             data=None,
                             headers=headers,
                             method="DELETE")