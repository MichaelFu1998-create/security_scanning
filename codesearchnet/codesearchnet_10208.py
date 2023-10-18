def get_ingest_status(self, dataset_id):
        """
        Returns the current status of dataset ingestion.  If any file uploaded to a dataset is in an error/failure state
        this endpoint will return error/failure.  If any files are still processing, will return processing.

        :param dataset_id: Dataset identifier
        :return: Status of dataset ingestion as a string
        """
        failure_message = "Failed to create dataset ingest status for dataset {}".format(dataset_id)
        response = self._get_success_json(
            self._get('v1/datasets/' + str(dataset_id) + '/ingest-status',
                            failure_message=failure_message))['data']

        if 'status' in response:
            return response['status']
        return ''