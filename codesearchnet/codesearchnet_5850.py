def get(self, folder_id, **queryparams):
        """
        Get information about a specific folder used to organize campaigns.

        :param folder_id: The unique id for the campaign folder.
        :type folder_id: :py:class:`str`
        :param queryparams: The query string parameters
        queryparams['fields'] = []
        queryparams['exclude_fields'] = []
        """
        self.folder_id = folder_id
        return self._mc_client._get(url=self._build_path(folder_id), **queryparams)