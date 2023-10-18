def get(self, **queryparams):
        """
        Get links to all other resources available in the API.

        :param queryparams: The query string parameters
        queryparams['fields'] = []
        queryparams['exclude_fields'] = []
        """
        return self._mc_client._get(url=self._build_path(), **queryparams)