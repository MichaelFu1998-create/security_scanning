def _data_analysis(self, data_view_id):
        """
        Data analysis endpoint.

        :param data_view_id: The model identifier (id number for data views)
        :type data_view_id: str
        :return: dictionary containing information about the data, e.g. dCorr and tsne
        """
        failure_message = "Error while retrieving data analysis for data view {}".format(data_view_id)
        return self._get_success_json(self._get(routes.data_analysis(data_view_id), failure_message=failure_message))