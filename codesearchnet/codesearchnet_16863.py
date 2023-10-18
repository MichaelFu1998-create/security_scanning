def get_template(self, template_id, version=None, timeout=None):
        """ API call to get a specific template """
        if (version):
            return self._api_request(
                self.TEMPLATES_VERSION_ENDPOINT % (template_id, version),
                self.HTTP_GET,
                timeout=timeout
            )
        else:
            return self._api_request(
                self.TEMPLATES_SPECIFIC_ENDPOINT % template_id,
                self.HTTP_GET,
                timeout=timeout
            )