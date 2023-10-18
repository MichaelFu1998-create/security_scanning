def create_or_update(self, store_id, customer_id, data):
        """
        Add or update a customer.

        :param store_id: The store id.
        :type store_id: :py:class:`str`
        :param customer_id: The id for the customer of a store.
        :type customer_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "id": string*,
            "email_address": string*,
            "opt_in_status": boolean
        }
        """
        self.store_id = store_id
        self.customer_id = customer_id
        if 'id' not in data:
            raise KeyError('The store customer must have an id')
        if 'email_address' not in data:
            raise KeyError('Each store customer must have an email_address')
        check_email(data['email_address'])
        if 'opt_in_status' not in data:
            raise KeyError('The store customer must have an opt_in_status')
        if data['opt_in_status'] not in [True, False]:
            raise TypeError('The opt_in_status must be True or False')
        return self._mc_client._put(url=self._build_path(store_id, 'customers', customer_id), data=data)