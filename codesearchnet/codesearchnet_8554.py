def _get_results(self, identity_provider, param_name, param_value, result_field_name):
        """
        Calls the third party auth api endpoint to get the mapping between usernames and remote ids.
        """
        try:
            kwargs = {param_name: param_value}
            returned = self.client.providers(identity_provider).users.get(**kwargs)
            results = returned.get('results', [])
        except HttpNotFoundError:
            LOGGER.error(
                'username not found for third party provider={provider}, {querystring_param}={id}'.format(
                    provider=identity_provider,
                    querystring_param=param_name,
                    id=param_value
                )
            )
            results = []

        for row in results:
            if row.get(param_name) == param_value:
                return row.get(result_field_name)
        return None