def create(self, config):
        """Create template config for specified template name.

        .. __: https://api.go.cd/current/#create-template-config

        Returns:
          Response: :class:`gocd.api.response.Response` object
        """

        assert config["name"] == self.name, "Given config is not for this template"

        data = self._json_encode(config)
        headers = self._default_headers()

        return self._request("",
                             ok_status=None,
                             data=data,
                             headers=headers)