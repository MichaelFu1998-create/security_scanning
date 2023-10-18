def _get_version(self):
        """Find requested version in GET request."""
        version = self._get_param(param="version", allowed_values=allowed_versions[self.params['service']],
                                  optional=True)
        if version is None and self._get_request_type() != "getcapabilities":
            raise OWSMissingParameterValue('Parameter "version" is missing', value="version")
        else:
            return version