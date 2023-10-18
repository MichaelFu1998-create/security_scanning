def update(self, list_id, subscriber_hash, data):
        """
        Update tags for a specific subscriber.

        The documentation lists only the tags request body parameter so it is
        being documented and error-checked as if it were required based on the
        description of the method.

        The data list needs to include a "status" key. This determines if the
        tag should be added or removed from the user:

        data = {
            'tags': [
                {'name': 'foo', 'status': 'active'},
                {'name': 'bar', 'status': 'inactive'}
            ]
        }

        :param list_id: The unique id for the list.
        :type list_id: :py:class:`str`
        :param subscriber_hash: The MD5 hash of the lowercase version of the
          list member’s email address.
        :type subscriber_hash: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "tags": list*
        }
        """
        subscriber_hash = check_subscriber_hash(subscriber_hash)
        self.list_id = list_id
        self.subscriber_hash = subscriber_hash
        if 'tags' not in data:
            raise KeyError('The list member tags must have a tag')
        response = self._mc_client._post(url=self._build_path(list_id, 'members', subscriber_hash, 'tags'), data=data)
        return response