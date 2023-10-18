def get(self, list_id, month, **queryparams):
        """
        Get a summary of a specific list’s growth activity for a specific month and year.

        :param list_id: The unique id for the list.
        :type list_id: :py:class:`str`
        :param month: A specific month of list growth history.
        :type month: :py:class:`str`
        :param queryparams: The query string parameters
        queryparams['fields'] = []
        queryparams['exclude_fields'] = []
        """
        self.list_id = list_id
        self.month = month
        return self._mc_client._get(url=self._build_path(list_id, 'growth-history', month), **queryparams)