def __get_ml_configuration_status(self, job_id):
        """
        After invoking the create_ml_configuration async method, you can use this method to
        check on the status of the builder job.

        :param job_id: The identifier returned from create_ml_configuration
        :return: Job status
        """

        failure_message = "Get status on ml configuration failed"
        response = self._get_success_json(self._get(
            'v1/descriptors/builders/simple/default/' + job_id + '/status', None, failure_message=failure_message))[
            'data']
        return response