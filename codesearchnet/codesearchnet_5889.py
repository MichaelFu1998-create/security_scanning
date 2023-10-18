def create_or_update(self, store_id, product_id, variant_id, data):
        """
        Add or update a product variant.

        :param store_id: The store id.
        :type store_id: :py:class:`str`
        :param product_id: The id for the product of a store.
        :type product_id: :py:class:`str`
        :param variant_id: The id for the product variant.
        :type variant_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "id": string*,
            "title": string*
        }
        """
        self.store_id = store_id
        self.product_id = product_id
        self.variant_id = variant_id
        if 'id' not in data:
             raise KeyError('The product variant must have an id')
        if 'title' not in data:
            raise KeyError('The product variant must have a title')
        return self._mc_client._put(
            url=self._build_path(store_id, 'products', product_id, 'variants', variant_id),
            data=data
        )