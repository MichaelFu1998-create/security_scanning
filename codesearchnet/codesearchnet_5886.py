def create(self, store_id, data):
        """
        Add a new customer to a store.

        :param store_id: The store id.
        :type store_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "id": string*,
            "email_address": string*,
            "opt_in_status": boolean*
        }
        """
        self.store_id = store_id
        if 'id' not in data:
            raise KeyError('The store customer must have an id')
        if 'email_address' not in data:
            raise KeyError('The store customer must have an email_address')
        check_email(data['email_address'])
        if 'opt_in_status' not in data:
            raise KeyError('The store customer must have an opt_in_status')
        if data['opt_in_status'] not in [True, False]:
            raise TypeError('The opt_in_status must be True or False')
        response = self._mc_client._post(url=self._build_path(store_id, 'customers'), data=data)
        if response is not None:
            self.customer_id = response['id']
        else:
            self.customer_id = None
        return response