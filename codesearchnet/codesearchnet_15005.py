def _get_version(self):
        """Find requested version in POST request."""
        if "version" in self.document.attrib:
            value = self.document.attrib["version"].lower()
            if value in allowed_versions[self.params['service']]:
                self.params["version"] = value
            else:
                raise OWSInvalidParameterValue("Version %s is not supported" % value, value="version")
        elif self._get_request_type() == "getcapabilities":
            self.params["version"] = None
        else:
            raise OWSMissingParameterValue('Parameter "version" is missing', value="version")
        return self.params["version"]