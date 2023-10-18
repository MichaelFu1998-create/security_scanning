def update(self, list_id, category_id, interest_id, data):
        """
        Update interests or ‘group names’ for a specific category.

        :param list_id: The unique id for the list.
        :type list_id: :py:class:`str`
        :param category_id: The unique id for the interest category.
        :type category_id: :py:class:`str`
        :param interest_id: The specific interest or ‘group name’.
        :type interest_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "name": string*
        }
        """
        self.list_id = list_id
        self.category_id = category_id
        self.interest_id = interest_id
        if 'name' not in data:
            raise KeyError('The list interest category interest must have a name')
        return self._mc_client._patch(
            url=self._build_path(list_id, 'interest-categories', category_id, 'interests', interest_id),
            data=data
        )