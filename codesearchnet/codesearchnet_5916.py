def delete(self, list_id, subscriber_hash):
        """
        Delete a member from a list.

        :param list_id: The unique id for the list.
        :type list_id: :py:class:`str`
        :param subscriber_hash: The MD5 hash of the lowercase version of the
          list member’s email address.
        :type subscriber_hash: :py:class:`str`
        """
        subscriber_hash = check_subscriber_hash(subscriber_hash)
        self.list_id = list_id
        self.subscriber_hash = subscriber_hash
        return self._mc_client._delete(url=self._build_path(list_id, 'members', subscriber_hash))