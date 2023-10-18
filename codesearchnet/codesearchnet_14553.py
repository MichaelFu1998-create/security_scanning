def create_group(self, group):
        """
        Creates a new group and set group privileges.

        :param      group: The group object to be created.
        :type       group: ``dict``

        """
        data = json.dumps(self._create_group_dict(group))

        response = self._perform_request(
            url='/um/groups',
            method='POST',
            data=data)

        return response