def predict(self, data_view_id, candidates, method="scalar", use_prior=True):
        """
        Predict endpoint. This simply wraps the async methods (submit and poll for status/results).

        :param data_view_id: The ID of the data view to use for prediction
        :type data_view_id: str
        :param candidates: A list of candidates to make predictions on
        :type candidates: list of dicts
        :param method: Method for propagating predictions through model graphs. "scalar" uses linearized uncertainty
        propagation, whereas "scalar_from_distribution" still returns scalar predictions but uses sampling to
        propagate uncertainty without a linear approximation.
        :type method: str ("scalar" or "scalar_from_distribution")
        :param use_prior:  Whether to apply prior values implied by the property descriptors
        :type use_prior: bool
        :return: The results of the prediction
        :rtype: list of :class:`PredictionResult`
        """

        uid = self.submit_predict_request(data_view_id, candidates, method, use_prior)

        while self.check_predict_status(data_view_id, uid)['status'] not in ["Finished", "Failed", "Killed"]:
            time.sleep(1)

        result = self.check_predict_status(data_view_id, uid)
        if result["status"] == "Finished":

            paired = zip(result["results"]["candidates"], result["results"]["loss"])
            prediction_result_format = [{k: (p[0][k], p[1][k]) for k in p[0].keys()} for p in paired]

            return list(map(
                lambda c: _get_prediction_result_from_candidate(c), prediction_result_format
            ))
        else:
            raise RuntimeError(
                "Prediction failed: UID={}, result={}".format(uid, result["status"])
            )