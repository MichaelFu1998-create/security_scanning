def create_ml_configuration(self, search_template, extract_as_keys, dataset_ids):
        """
        This method will spawn a server job to create a default ML configuration based on a search template and
        the extract as keys.
        This function will submit the request to build, and wait for the configuration to finish before returning.

        :param search_template: A search template defining the query (properties, datasets etc)
        :param extract_as_keys: Array of extract-as keys defining the descriptors
        :param dataset_ids: Array of dataset identifiers to make search template from
        :return: An identifier used to request the status of the builder job (get_ml_configuration_status)
        """
        data = {
            "search_template":
                search_template,
            "extract_as_keys":
                extract_as_keys
        }

        failure_message = "ML Configuration creation failed"
        config_job_id = self._get_success_json(self._post_json(
            'v1/descriptors/builders/simple/default/trigger', data, failure_message=failure_message))['data'][
            'result']['uid']

        while True:
            config_status = self.__get_ml_configuration_status(config_job_id)
            print('Configuration status: ', config_status)
            if config_status['status'] == 'Finished':
                ml_config = self.__convert_response_to_configuration(config_status['result'], dataset_ids)
                return ml_config
            time.sleep(5)