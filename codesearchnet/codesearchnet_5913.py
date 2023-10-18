def create(self, list_id, data):
        """
        Add a new member to the list.

        :param list_id: The unique id for the list.
        :type list_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "status": string*, (Must be one of 'subscribed', 'unsubscribed', 'cleaned',
                'pending', or 'transactional')
            "email_address": string*
        }
        """
        self.list_id = list_id
        if 'status' not in data:
            raise KeyError('The list member must have a status')
        if data['status'] not in ['subscribed', 'unsubscribed', 'cleaned', 'pending', 'transactional']:
            raise ValueError('The list member status must be one of "subscribed", "unsubscribed", "cleaned", '
                             '"pending", or "transactional"')
        if 'email_address' not in data:
            raise KeyError('The list member must have an email_address')
        check_email(data['email_address'])
        response = self._mc_client._post(url=self._build_path(list_id, 'members'), data=data)
        if response is not None:
            self.subscriber_hash = response['id']
        else:
            self.subscriber_hash = None
        return response