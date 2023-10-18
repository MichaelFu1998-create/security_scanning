def delete_course_completion(self, user_id, payload):  # pylint: disable=unused-argument
        """
        Delete a completion status previously sent to the Degreed Completion Status endpoint

        Args:
            user_id: Unused.
            payload: JSON encoded object (serialized from DegreedLearnerDataTransmissionAudit)
                containing the required completion status fields for deletion per Degreed documentation.

        Returns:
            A tuple containing the status code and the body of the response.
        Raises:
            HTTPError: if we received a failure response code from Degreed
        """
        return self._delete(
            urljoin(
                self.enterprise_configuration.degreed_base_url,
                self.global_degreed_config.completion_status_api_path
            ),
            payload,
            self.COMPLETION_PROVIDER_SCOPE
        )