def __generate_search_template(self, dataset_ids):
        """
        Generates a default search templates from the available columns in the dataset ids given.

        :param dataset_ids: The id of the dataset to retrieve files from
        :type dataset_ids: list of int
        :return: A search template based on the columns in the datasets given
        """

        data = {
            "dataset_ids":
                dataset_ids
        }

        failure_message = "Failed to generate a search template from columns in dataset(s) {}".format(dataset_ids)

        return self._get_success_json(self._post_json(
            'v1/search_templates/builders/from-dataset-ids', data, failure_message=failure_message))['data']