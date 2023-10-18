def _sync_content_metadata(self, serialized_data):
        """
        Create/update/delete content metadata records using the SuccessFactors OCN Course Import API endpoint.

        Arguments:
            serialized_data: Serialized JSON string representing a list of content metadata items.

        Raises:
            ClientError: If SuccessFactors API call fails.
        """
        url = self.enterprise_configuration.sapsf_base_url + self.global_sap_config.course_api_path
        try:
            status_code, response_body = self._call_post_with_session(url, serialized_data)
        except requests.exceptions.RequestException as exc:
            raise ClientError(
                'SAPSuccessFactorsAPIClient request failed: {error} {message}'.format(
                    error=exc.__class__.__name__,
                    message=str(exc)
                )
            )

        if status_code >= 400:
            raise ClientError(
                'SAPSuccessFactorsAPIClient request failed with status {status_code}: {message}'.format(
                    status_code=status_code,
                    message=response_body
                )
            )