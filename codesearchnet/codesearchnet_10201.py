def kill_design_run(self, data_view_id, run_uuid):
        """
        Kills an in progress experimental design run

        :param data_view_id: The ID number of the data view to which the
            run belongs, as a string
        :type data_view_id: str
        :param run_uuid: The UUID of the design run to kill
        :type run_uuid: str
        :return: The UUID of the design run
        """

        url = routes.kill_data_view_design_run(data_view_id, run_uuid)

        response = self._delete(url).json()
        return response["data"]["uid"]