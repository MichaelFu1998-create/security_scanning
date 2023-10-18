def _sync_content_metadata(self, serialized_data, http_method):
        """
        Synchronize content metadata using the Degreed course content API.

        Args:
            serialized_data: JSON-encoded object containing content metadata.
            http_method: The HTTP method to use for the API request.

        Raises:
            ClientError: If Degreed API request fails.
        """
        try:
            status_code, response_body = getattr(self, '_' + http_method)(
                urljoin(self.enterprise_configuration.degreed_base_url, self.global_degreed_config.course_api_path),
                serialized_data,
                self.CONTENT_PROVIDER_SCOPE
            )
        except requests.exceptions.RequestException as exc:
            raise ClientError(
                'DegreedAPIClient request failed: {error} {message}'.format(
                    error=exc.__class__.__name__,
                    message=str(exc)
                )
            )

        if status_code >= 400:
            raise ClientError(
                'DegreedAPIClient request failed with status {status_code}: {message}'.format(
                    status_code=status_code,
                    message=response_body
                )
            )