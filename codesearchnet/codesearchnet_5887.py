def get(self, store_id, customer_id, **queryparams):
        """
        Get information about a specific customer.

        :param store_id: The store id.
        :type store_id: :py:class:`str`
        :param customer_id: The id for the customer of a store.
        :type customer_id: :py:class:`str`
        :param queryparams: The query string parameters
        queryparams['fields'] = []
        queryparams['exclude_fields'] = []
        """
        self.store_id = store_id
        self.customer_id = customer_id
        return self._mc_client._get(url=self._build_path(store_id, 'customers', customer_id), **queryparams)