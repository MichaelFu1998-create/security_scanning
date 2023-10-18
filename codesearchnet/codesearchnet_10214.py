def update_dataset(self, dataset_id, name=None, description=None, public=None):
        """
        Update a data set.

        :param dataset_id: The ID of the dataset to update
        :type dataset_id: int
        :param name: name of the dataset
        :type name: str
        :param description: description for the dataset
        :type description: str
        :param public: A boolean indicating whether or not the dataset should
            be public.
        :type public: bool
        :return: The updated dataset.
        :rtype: :class:`Dataset`
        """
        data = {
            "public": _convert_bool_to_public_value(public)
        }

        if name:
            data["name"] = name
        if description:
            data["description"] = description

        dataset = {"dataset": data}
        failure_message = "Failed to update dataset {}".format(dataset_id)
        response = self._get_success_json(self._post_json(routes.update_dataset(dataset_id), data=dataset, failure_message=failure_message))

        return _dataset_from_response_dict(response)