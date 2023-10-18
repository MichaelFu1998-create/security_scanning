def create_ml_configuration_from_datasets(self, dataset_ids):
        """
        Creates an ml configuration from dataset_ids and extract_as_keys

        :param dataset_ids: Array of dataset identifiers to make search template from
        :return: An identifier used to request the status of the builder job (get_ml_configuration_status)
        """
        available_columns = self.search_template_client.get_available_columns(dataset_ids)

        # Create a search template from dataset ids
        search_template = self.search_template_client.create(dataset_ids, available_columns)
        return self.create_ml_configuration(search_template, available_columns, dataset_ids)