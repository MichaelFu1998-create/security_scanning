def create_dataset(self, name=None, description=None, public=False):
        """
        Create a new data set.

        :param name: name of the dataset
        :type name: str
        :param description: description for the dataset
        :type description: str
        :param public: A boolean indicating whether or not the dataset should be public.
        :type public: bool
        :return: The newly created dataset.
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
        failure_message = "Unable to create dataset"
        result = self._get_success_json(self._post_json(routes.create_dataset(), dataset, failure_message=failure_message))

        return _dataset_from_response_dict(result)