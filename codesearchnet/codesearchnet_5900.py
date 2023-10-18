def create(self, store_id, product_id, data):
        """
        Add a new image to the product.

        :param store_id: The store id.
        :type store_id: :py:class:`str`
        :param product_id: The id for the product of a store.
        :type product_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "id": string*,
            "url": string*
        }
        """
        self.store_id = store_id
        self.product_id = product_id
        if 'id' not in data:
            raise KeyError('The product image must have an id')
        if 'title' not in data:
            raise KeyError('The product image must have a url')
        response = self._mc_client._post(url=self._build_path(store_id, 'products', product_id, 'images'), data=data)
        if response is not None:
            self.image_id = response['id']
        else:
            self.image_id = None
        return response