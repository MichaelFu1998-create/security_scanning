def __convert_response_to_configuration(self, result_blob, dataset_ids):
        """
        Utility function to turn the result object from the configuration builder endpoint into something that
        can be used directly as a configuration.

        :param result_blob: Nested dicts representing the possible descriptors
        :param dataset_ids: Array of dataset identifiers to make search template from
        :return: An object suitable to be used as a parameter to data view create
        """

        builder = DataViewBuilder()
        builder.dataset_ids(dataset_ids)
        for i, (k, v) in enumerate(result_blob['descriptors'].items()):
            try:
                descriptor = self.__snake_case(v[0])
                print(json.dumps(descriptor))
                descriptor['descriptor_key'] = k
                builder.add_raw_descriptor(descriptor)
            except IndexError:
                pass

        for i, (k, v) in enumerate(result_blob['types'].items()):
            builder.set_role(k, v.lower())

        return builder.build()