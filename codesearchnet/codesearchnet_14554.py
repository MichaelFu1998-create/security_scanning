def update_group(self, group_id, **kwargs):
        """
        Updates a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        """
        properties = {}

        # make the key camel-case transformable
        if 'create_datacenter' in kwargs:
            kwargs['create_data_center'] = kwargs.pop('create_datacenter')

        for attr, value in kwargs.items():
            properties[self._underscore_to_camelcase(attr)] = value

        data = {
            "properties": properties
        }

        response = self._perform_request(
            url='/um/groups/%s' % group_id,
            method='PUT',
            data=json.dumps(data))

        return response