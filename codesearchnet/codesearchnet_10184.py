def get(self, data_view_id):
        """
        Gets basic information about a view

        :param data_view_id: Identifier of the data view
        :return: Metadata about the view as JSON
        """

        failure_message = "Dataview get failed"
        return self._get_success_json(self._get(
            'v1/data_views/' + data_view_id, None, failure_message=failure_message))['data']['data_view']