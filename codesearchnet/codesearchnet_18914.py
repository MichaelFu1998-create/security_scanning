def add_scalar_data(self, token, community_id, producer_display_name,
                        metric_name, producer_revision, submit_time, value,
                        **kwargs):
        """
        Create a new scalar data point.

        :param token: A valid token for the user in question.
        :type token: string
        :param community_id: The id of the community that owns the producer.
        :type community_id: int | long
        :param producer_display_name: The display name of the producer.
        :type producer_display_name: string
        :param metric_name: The metric name that identifies which trend this
            point belongs to.
        :type metric_name: string
        :param producer_revision: The repository revision of the producer that
            produced this value.
        :type producer_revision: int | long | string
        :param submit_time: The submit timestamp. Must be parsable with PHP
            strtotime().
        :type submit_time: string
        :param value: The value of the scalar.
        :type value: float
        :param config_item_id: (optional) If this value pertains to a specific
            configuration item, pass its id here.
        :type config_item_id: int | long
        :param test_dataset_id: (optional) If this value pertains to a
            specific test dataset, pass its id here.
        :type test_dataset_id: int | long
        :param truth_dataset_id: (optional) If this value pertains to a
            specific ground truth dataset, pass its id here.
        :type truth_dataset_id: int | long
        :param silent: (optional) If true, do not perform threshold-based email
            notifications for this scalar.
        :type silent: bool
        :param unofficial: (optional) If true, creates an unofficial scalar
            visible only to the user performing the submission.
        :type unofficial: bool
        :param build_results_url: (optional) A URL for linking to build results
            for this submission.
        :type build_results_url: string
        :param branch: (optional) The branch name in the source repository for
            this submission.
        :type branch: string
        :param submission_id: (optional) The id of the submission.
        :type submission_id: int | long
        :param submission_uuid: (optional) The uuid of the submission. If one
            does not exist, it will be created.
        :type submission_uuid: string
        :type branch: string
        :param params: (optional) Any key/value pairs that should be displayed
            with this scalar result.
        :type params: dict
        :param extra_urls: (optional) Other URL's that should be displayed with
            with this scalar result. Each element of the list should be a dict
            with the following keys: label, text, href
        :type extra_urls: list[dict]
        :param unit: (optional) The unit of the scalar value.
        :type unit: string
        :param reproduction_command: (optional) The command to reproduce this
            scalar.
        :type reproduction_command: string
        :returns: The scalar object that was created.
        :rtype: dict
        """
        parameters = dict()
        parameters['token'] = token
        parameters['communityId'] = community_id
        parameters['producerDisplayName'] = producer_display_name
        parameters['metricName'] = metric_name
        parameters['producerRevision'] = producer_revision
        parameters['submitTime'] = submit_time
        parameters['value'] = value
        optional_keys = [
            'config_item_id', 'test_dataset_id', 'truth_dataset_id', 'silent',
            'unofficial', 'build_results_url', 'branch', 'extra_urls',
            'params', 'submission_id', 'submission_uuid', 'unit',
            'reproduction_command'
        ]
        for key in optional_keys:
            if key in kwargs:
                if key == 'config_item_id':
                    parameters['configItemId'] = kwargs[key]
                elif key == 'test_dataset_id':
                    parameters['testDatasetId'] = kwargs[key]
                elif key == 'truth_dataset_id':
                    parameters['truthDatasetId'] = kwargs[key]
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
                elif key == 'submission_id':
                    parameters['submissionId'] = kwargs[key]
                elif key == 'submission_uuid':
                    parameters['submissionUuid'] = kwargs[key]
                elif key == 'unit':
                    parameters['unit'] = kwargs[key]
                elif key == 'reproduction_command':
                    parameters['reproductionCommand'] = kwargs[key]
                else:
                    parameters[key] = kwargs[key]
        response = self.request('midas.tracker.scalar.add', parameters)
        return response