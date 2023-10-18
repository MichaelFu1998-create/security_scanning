def create_or_update(self, list_id, subscriber_hash, data):
        """
        Add or update a list member.

        :param list_id: The unique id for the list.
        :type list_id: :py:class:`str`
        :param subscriber_hash: The MD5 hash of the lowercase version of the
            list member’s email address.
        :type subscriber_hash: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "email_address": string*,
            "status_if_new": string* (Must be one of 'subscribed',
                'unsubscribed', 'cleaned', 'pending', or 'transactional')
        }
        """
        subscriber_hash = check_subscriber_hash(subscriber_hash)
        self.list_id = list_id
        self.subscriber_hash = subscriber_hash
        if 'email_address' not in data:
            raise KeyError('The list member must have an email_address')
        check_email(data['email_address'])
        if 'status_if_new' not in data:
            raise KeyError('The list member must have a status_if_new')
        if data['status_if_new'] not in ['subscribed', 'unsubscribed', 'cleaned', 'pending', 'transactional']:
            raise ValueError('The list member status_if_new must be one of "subscribed", "unsubscribed", "cleaned", '
                             '"pending", or "transactional"')
        return self._mc_client._put(url=self._build_path(list_id, 'members', subscriber_hash), data=data)