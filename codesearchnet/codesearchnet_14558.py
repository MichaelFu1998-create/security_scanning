def add_share(self, group_id, resource_id, **kwargs):
        """
        Shares a resource through a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      resource_id: The unique ID of the resource.
        :type       resource_id: ``str``

        """
        properties = {}

        for attr, value in kwargs.items():
            properties[self._underscore_to_camelcase(attr)] = value

        data = {
            "properties": properties
        }

        response = self._perform_request(
            url='/um/groups/%s/shares/%s' % (group_id, resource_id),
            method='POST',
            data=json.dumps(data))

        return response