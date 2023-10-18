def get_available_columns(self, dataset_ids):
        """
        Retrieves the set of columns from the combination of dataset ids given

        :param dataset_ids: The id of the dataset to retrieve columns from
        :type dataset_ids: list of int
        :return: A list of column names from the dataset ids given.
        :rtype: list of str
        """
        if not isinstance(dataset_ids, list):
            dataset_ids = [dataset_ids]

        data = {
            "dataset_ids":
                dataset_ids
        }

        failure_message = "Failed to get available columns in dataset(s) {}".format(dataset_ids)

        return self._get_success_json(self._post_json(
            'v1/datasets/get-available-columns', data, failure_message=failure_message))['data']