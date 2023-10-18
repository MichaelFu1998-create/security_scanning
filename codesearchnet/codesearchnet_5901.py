def all(self, store_id, product_id, get_all=False, **queryparams):
        """
        Get information about a product’s images.

        :param store_id: The store id.
        :type store_id: :py:class:`str`
        :param product_id: The id for the product of a store.
        :type product_id: :py:class:`str`
        :param get_all: Should the query get all results
        :type get_all: :py:class:`bool`
        :param queryparams: The query string parameters
        queryparams['fields'] = []
        queryparams['exclude_fields'] = []
        queryparams['count'] = integer
        queryparams['offset'] = integer
        """
        self.store_id = store_id
        self.product_id = product_id
        self.image_id = None
        if get_all:
            return self._iterate(url=self._build_path(store_id, 'products', product_id, 'images'), **queryparams)
        else:
            return self._mc_client._post(url=self._build_path(store_id, 'products', product_id, 'images'), **queryparams)