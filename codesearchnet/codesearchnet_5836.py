def get(self, template_id, **queryparams):
        """
        Get information about a specific template.

        :param template_id: The unique id for the template.
        :type template_id: :py:class:`str`
        :param queryparams: The query string parameters
        queryparams['fields'] = []
        queryparams['exclude_fields'] = []
        """
        self.template_id = template_id
        return self._mc_client._get(url=self._build_path(template_id), **queryparams)