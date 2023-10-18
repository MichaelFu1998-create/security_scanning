def update(self, id, configuration, name, description):
        """
        Updates an existing data view from the search template and ml template given

        :param id: Identifier for the data view.  This returned from the create method.
        :param configuration: Information to construct the data view from (eg descriptors, datasets etc)
        :param name: Name of the data view
        :param description: Description for the data view
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

        self._patch_json(
            'v1/data_views/' + id, data, failure_message=failure_message)