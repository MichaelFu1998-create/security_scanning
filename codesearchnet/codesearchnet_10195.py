def submit_predict_request(self, data_view_id, candidates, prediction_source='scalar', use_prior=True):
        """
        Submits an async prediction request.

        :param data_view_id: The id returned from create
        :param candidates: Array of candidates
        :param prediction_source: 'scalar' or 'scalar_from_distribution'
        :param use_prior: True to use prior prediction, otherwise False
        :return: Predict request Id (used to check status)
        """

        data = {
            "prediction_source":
                prediction_source,
            "use_prior":
                use_prior,
            "candidates":
                candidates
        }

        failure_message = "Configuration creation failed"
        post_url = 'v1/data_views/' + str(data_view_id) + '/predict/submit'
        return self._get_success_json(
            self._post_json(post_url, data, failure_message=failure_message)
        )['data']['uid']