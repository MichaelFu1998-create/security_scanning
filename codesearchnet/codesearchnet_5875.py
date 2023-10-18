def all(self, template_id, **queryparams):
        """
        Get the sections that you can edit in a template, including each
        section’s default content.

        :param template_id: The unique id for the template.
        :type template_id: :py:class:`str`
        :param queryparams: The query string parameters
        queryparams['fields'] = []
        queryparams['exclude_fields'] = []
        """
        self.template_id = template_id
        return self._mc_client._get(url=self._build_path(template_id, 'default-content'), **queryparams)