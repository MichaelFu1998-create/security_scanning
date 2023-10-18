def create(self, store_id, order_id, data):
        """
        Add a new line item to an existing order.

        :param store_id: The store id.
        :type store_id: :py:class:`str`
        :param order_id: The id for the order in a store.
        :type order_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "id": string*,
            "product_id": string*,
            "product_variant_id": string*,
            "quantity": integer*,
            "price": number*
        }
        """
        self.store_id = store_id
        self.order_id = order_id
        if 'id' not in data:
            raise KeyError('The order line must have an id')
        if 'product_id' not in data:
            raise KeyError('The order line must have a product_id')
        if 'product_variant_id' not in data:
            raise KeyError('The order line must have a product_variant_id')
        if 'quantity' not in data:
            raise KeyError('The order line must have a quantity')
        if 'price' not in data:
            raise KeyError('The order line must have a price')
        response = self._mc_client._post(url=self._build_path(store_id, 'orders', order_id, 'lines'))
        if response is not None:
            self.line_id = response['id']
        else:
            self.line_id = None
        return response