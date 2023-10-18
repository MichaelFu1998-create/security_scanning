def create(self, list_id, subscriber_hash, data):
        """
        Add a new note for a specific subscriber.

        The documentation lists only the note request body parameter so it is
        being documented and error-checked as if it were required based on the
        description of the method.

        :param list_id: The unique id for the list.
        :type list_id: :py:class:`str`
        :param subscriber_hash: The MD5 hash of the lowercase version of the
          list member’s email address.
        :type subscriber_hash: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "note": string*
        }
        """
        subscriber_hash = check_subscriber_hash(subscriber_hash)
        self.list_id = list_id
        self.subscriber_hash = subscriber_hash
        if 'note' not in data:
            raise KeyError('The list member note must have a note')
        response = self._mc_client._post(url=self._build_path(list_id, 'members', subscriber_hash, 'notes'), data=data)
        if response is not None:
            self.note_id = response['id']
        else:
            self.note_id = None
        return response