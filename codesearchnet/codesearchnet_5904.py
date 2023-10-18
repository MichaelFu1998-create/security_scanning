def create(self, store_id, data):
        """
        Add a new order to a store.

        :param store_id: The store id.
        :type store_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "id": string*,
            "customer": object*
            {
                "'id": string*
            },
            "curency_code": string*,
            "order_total": number*,
            "lines": array*
            [
                {
                    "id": string*,
                    "product_id": string*,
                    "product_variant_id": string*,
                    "quantity": integer*,
                    "price": number*
                }
            ]
        }
        """
        self.store_id = store_id
        if 'id' not in data:
            raise KeyError('The order must have an id')
        if 'customer' not in data:
            raise KeyError('The order must have a customer')
        if 'id' not in data['customer']:
            raise KeyError('The order customer must have an id')
        if 'currency_code' not in data:
            raise KeyError('The order must have a currency_code')
        if not re.match(r"^[A-Z]{3}$", data['currency_code']):
            raise ValueError('The currency_code must be a valid 3-letter ISO 4217 currency code')
        if 'order_total' not in data:
            raise KeyError('The order must have an order_total')
        if 'lines' not in data:
            raise KeyError('The order must have at least one order line')
        for line in data['lines']:
            if 'id' not in line:
                raise KeyError('Each order line must have an id')
            if 'product_id' not in line:
                raise KeyError('Each order line must have a product_id')
            if 'product_variant_id' not in line:
                raise KeyError('Each order line must have a product_variant_id')
            if 'quantity' not in line:
                raise KeyError('Each order line must have a quantity')
            if 'price' not in line:
                raise KeyError('Each order line must have a price')
        response = self._mc_client._post(url=self._build_path(store_id, 'orders'), data=data)
        if response is not None:
            self.order_id = response['id']
        else:
            self.order_id = None
        return response