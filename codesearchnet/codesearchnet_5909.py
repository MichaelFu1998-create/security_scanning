def create(self, list_id, category_id, data):
        """
        Create a new interest or ‘group name’ for a specific category.

        The documentation lists only the name request body parameter so it is
        being documented and error-checked as if it were required based on the
        description of the method.

        :param list_id: The unique id for the list.
        :type list_id: :py:class:`str`
        :param category_id: The unique id for the interest category.
        :type category_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "name": string*
        }
        """
        self.list_id = list_id
        self.category_id = category_id
        if 'name' not in data:
            raise KeyError('The list interest category interest must have a name')
        response =  self._mc_client._post(
            url=self._build_path(list_id, 'interest-categories', category_id, 'interests'),
            data=data
        )
        if response is not None:
            self.interest_id = response['id']
        else:
            self.interest_id = None
        return response