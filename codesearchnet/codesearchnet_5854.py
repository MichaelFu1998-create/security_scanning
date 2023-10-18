def get(self, file_id, **queryparams):
        """
        Get information about a specific file in the File Manager.

        :param file_id: The unique id for the File Manager file.
        :type file_id: :py:class:`str`
        :param queryparams: The query string parameters
        queryparams['fields'] = []
        queryparams['exclude_fields'] = []
        """
        self.file_id = file_id
        return self._mc_client._get(url=self._build_path(file_id), **queryparams)