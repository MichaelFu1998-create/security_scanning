def get_data_view_service_status(self, data_view_id):
        """
        Retrieves the status for all of the services associated with a data view:
            - predict
            - experimental_design
            - data_reports
            - model_reports

        :param data_view_id: The ID number of the data view to which the
            run belongs, as a string
        :type data_view_id: str
        :return: A :class:`DataViewStatus`
        :rtype: DataViewStatus
        """

        url = "data_views/{}/status".format(data_view_id)

        response = self._get(url).json()
        result = response["data"]["status"]

        return DataViewStatus(
            predict=ServiceStatus.from_response_dict(result["predict"]),
            experimental_design=ServiceStatus.from_response_dict(result["experimental_design"]),
            data_reports=ServiceStatus.from_response_dict(result["data_reports"]),
            model_reports=ServiceStatus.from_response_dict(result["model_reports"])
        )