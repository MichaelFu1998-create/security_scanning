def create(self, configuration, name, description):
        """
        Creates a data view from the search template and ml template given

        :param configuration: Information to construct the data view from (eg descriptors, datasets etc)
        :param name: Name of the data view
        :param description: Description for the data view
        :return: The data view id
        """

        data = {
            "configuration":
                configuration,
            "name":
                name,
            "description":
                description
        }

        failure_message = "Dataview creation failed"

        result = self._get_success_json(self._post_json(
            'v1/data_views', data, failure_message=failure_message))
        data_view_id = result['data']['id']

        return data_view_id