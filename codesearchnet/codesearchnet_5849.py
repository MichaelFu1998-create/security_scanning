def create(self, store_id, data):
        """
        Add new promo rule to a store

        :param store_id: The store id
        :type store_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict'
        data = {
            "id": string*,
            "title": string,
            "description": string*,
            "starts_at": string,
            "ends_at": string,
            "amount": number*,
            "type": string*,
            "target": string*,
            "enabled": boolean,
            "created_at_foreign": string,
            "updated_at_foreign": string,
        }
        """
        self.store_id = store_id
        if 'id' not in data:
            raise KeyError('The promo rule must have an id')
        if 'description' not in data:
            raise KeyError('This promo rule must have a description')
        if 'amount' not in data:
            raise KeyError('This promo rule must have an amount')
        if 'target' not in data:
            raise KeyError('This promo rule must apply to a target (example per_item, total, or shipping')
        response = self._mc_client._post(url=self._build_path(store_id, 'promo-rules'), data=data)

        if response is not None:
            return response