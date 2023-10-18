def check_predict_status(self, view_id, predict_request_id):
        """
        Returns a string indicating the status of the prediction job

        :param view_id: The data view id returned from data view create
        :param predict_request_id: The id returned from predict
        :return: Status data, also includes results if state is finished
        """

        failure_message = "Get status on predict failed"

        bare_response = self._get_success_json(self._get(
            'v1/data_views/' + str(view_id) + '/predict/' + str(predict_request_id) + '/status',
            None, failure_message=failure_message))

        result = bare_response["data"]
        # result.update({"message": bare_response["message"]})

        return result