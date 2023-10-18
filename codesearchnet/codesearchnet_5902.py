def get(self, store_id, product_id, image_id, **queryparams):
        """
        Get information about a specific product image.

        :param store_id: The store id.
        :type store_id: :py:class:`str`
        :param product_id: The id for the product of a store.
        :type product_id: :py:class:`str`
        :param image_id: The id for the product image.
        :type image_id: :py:class:`str`
        :param queryparams: The query string parameters
        queryparams['fields'] = []
        queryparams['exclude_fields'] = []
        """
        self.store_id = store_id
        self.product_id = product_id
        self.image_id = image_id
        return self._mc_client._post(
            url=self._build_path(store_id, 'products', product_id, 'images', image_id),
            **queryparams
        )