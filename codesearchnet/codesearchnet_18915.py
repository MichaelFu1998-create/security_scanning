def upload_json_results(self, token, filepath, community_id,
                            producer_display_name, metric_name,
                            producer_revision, submit_time, **kwargs):
        """
        Upload a JSON file containing numeric scoring results to be added as
        scalars. File is parsed and then deleted from the server.

        :param token: A valid token for the user in question.
        :param filepath: The path to the JSON file.
        :param community_id: The id of the community that owns the producer.
        :param producer_display_name: The display name of the producer.
        :param producer_revision: The repository revision of the producer
            that produced this value.
        :param submit_time: The submit timestamp. Must be parsable with PHP
            strtotime().
        :param config_item_id: (optional) If this value pertains to a specific
            configuration item, pass its id here.
        :param test_dataset_id: (optional) If this value pertains to a
            specific test dataset, pass its id here.
        :param truth_dataset_id: (optional) If this value pertains to a
            specific ground truth dataset, pass its id here.
        :param parent_keys: (optional) Semicolon-separated list of parent keys
            to look for numeric results under. Use '.' to denote nesting, like
            in normal javascript syntax.
        :param silent: (optional) If true, do not perform threshold-based email
            notifications for this scalar.
        :param unofficial: (optional) If true, creates an unofficial scalar
            visible only to the user performing the submission.
        :param build_results_url: (optional) A URL for linking to build results
            for this submission.
        :param branch: (optional) The branch name in the source repository for
            this submission.
        :param params: (optional) Any key/value pairs that should be displayed
            with this scalar result.
        :type params: dict
        :param extra_urls: (optional) Other URL's that should be displayed with
            with this scalar result. Each element of the list should be a dict
            with the following keys: label, text, href
        :type extra_urls: list of dicts
        :returns: The list of scalars that were created.
        """
        parameters = dict()
        parameters['token'] = token
        parameters['communityId'] = community_id
        parameters['producerDisplayName'] = producer_display_name
        parameters['metricName'] = metric_name
        parameters['producerRevision'] = producer_revision
        parameters['submitTime'] = submit_time
        optional_keys = [
            'config_item_id', 'test_dataset_id', 'truth_dataset_id', 'silent',
            'unofficial', 'build_results_url', 'branch', 'extra_urls',
            'params']
        for key in optional_keys:
            if key in kwargs:
                if key == 'config_item_id':
                    parameters['configItemId'] = kwargs[key]
                elif key == 'test_dataset_id':
                    parameters['testDatasetId'] = kwargs[key]
                elif key == 'truth_dataset_id':
                    parameters['truthDatasetId'] = kwargs[key]
                elif key == 'parent_keys':
                    parameters['parentKeys'] = kwargs[key]
                elif key == 'build_results_url':
                    parameters['buildResultsUrl'] = kwargs[key]
                elif key == 'extra_urls':
                    parameters['extraUrls'] = json.dumps(kwargs[key])
                elif key == 'params':
                    parameters[key] = json.dumps(kwargs[key])
                elif key == 'silent':
                    if kwargs[key]:
                        parameters[key] = kwargs[key]
                elif key == 'unofficial':
                    if kwargs[key]:
                        parameters[key] = kwargs[key]
                else:
                    parameters[key] = kwargs[key]
        file_payload = open(filepath, 'rb')
        response = self.request('midas.tracker.results.upload.json',
                                parameters, file_payload)
        return response