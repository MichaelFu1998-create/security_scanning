def create_dataset_version(self, dataset_id):
        """
        Create a new data set version.

        :param dataset_id: The ID of the dataset for which the version must be bumped.
        :type dataset_id: int
        :return: The new dataset version.
        :rtype: :class:`DatasetVersion`
        """
        failure_message = "Failed to create dataset version for dataset {}".format(dataset_id)
        number = self._get_success_json(self._post_json(routes.create_dataset_version(dataset_id), data={}, failure_message=failure_message))['dataset_scoped_id']

        return DatasetVersion(number=number)