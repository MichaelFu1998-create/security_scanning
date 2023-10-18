def _load_data(self, resource, default=DEFAULT_VALUE_SAFEGUARD, **kwargs):
        """
        Load data from API client.

        Arguments:
            resource(string): type of resource to load
            default(any): value to return if API query returned empty result. Sensible values: [], {}, None etc.

        Returns:
            dict: Deserialized response from Course Catalog API

        """
        default_val = default if default != self.DEFAULT_VALUE_SAFEGUARD else {}
        try:
            return get_edx_api_data(
                api_config=CatalogIntegration.current(),
                resource=resource,
                api=self.client,
                **kwargs
            ) or default_val
        except (SlumberBaseException, ConnectionError, Timeout) as exc:
            LOGGER.exception(
                'Failed to load data from resource [%s] with kwargs [%s] due to: [%s]',
                resource, kwargs, str(exc)
            )
            return default_val