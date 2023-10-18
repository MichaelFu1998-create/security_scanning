def update(self, template_id, data):
        """
        Update the name, HTML, or folder_id of an existing template.

        :param template_id: The unique id for the template.
        :type template_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "name": string*,
            "html": string*
        }
        """
        if 'name' not in data:
            raise KeyError('The template must have a name')
        if 'html' not in data:
            raise KeyError('The template must have html')
        self.template_id = template_id
        return self._mc_client._patch(url=self._build_path(template_id), data=data)