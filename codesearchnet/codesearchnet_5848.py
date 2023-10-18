def get(self, app_id, **queryparams):
        """
        Get information about a specific authorized application

        :param app_id: The unique id for the connected authorized application
        :type app_id: :py:class:`str`
        :param queryparams: The query string parameters
        queryparams['fields'] = []
        queryparams['exclude_fields'] = []
        """
        self.app_id = app_id
        return self._mc_client._get(url=self._build_path(app_id), **queryparams)