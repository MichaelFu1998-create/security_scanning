def delete(self, template_id):
        """
        Delete a specific template.

        :param template_id: The unique id for the template.
        :type template_id: :py:class:`str`
        """
        self.template_id = template_id
        return self._mc_client._delete(url=self._build_path(template_id))