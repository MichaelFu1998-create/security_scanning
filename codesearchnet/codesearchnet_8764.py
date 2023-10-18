def create_course_completion(self, user_id, payload):
        """
        Send a completion status payload to the SuccessFactors OCN Completion Status endpoint

        Args:
            user_id (str): The sap user id that the completion status is being sent for.
            payload (str): JSON encoded object (serialized from SapSuccessFactorsLearnerDataTransmissionAudit)
                containing completion status fields per SuccessFactors documentation.

        Returns:
            The body of the response from SAP SuccessFactors, if successful
        Raises:
            HTTPError: if we received a failure response code from SAP SuccessFactors
        """
        url = self.enterprise_configuration.sapsf_base_url + self.global_sap_config.completion_status_api_path
        return self._call_post_with_user_override(user_id, url, payload)