def _get_oauth_access_token(self, client_id, client_secret, user_id, user_password, scope):
        """ Retrieves OAuth 2.0 access token using the client credentials grant.

        Args:
            client_id (str): API client ID
            client_secret (str): API client secret
            user_id (str): Degreed company ID
            user_password (str): Degreed user password
            scope (str): Must be one of the scopes Degreed expects:
                        - `CONTENT_PROVIDER_SCOPE`
                        - `COMPLETION_PROVIDER_SCOPE`

        Returns:
            tuple: Tuple containing access token string and expiration datetime.
        Raises:
            HTTPError: If we received a failure response code from Degreed.
            RequestException: If an unexpected response format was received that we could not parse.
        """
        response = requests.post(
            urljoin(self.enterprise_configuration.degreed_base_url, self.global_degreed_config.oauth_api_path),
            data={
                'grant_type': 'password',
                'username': user_id,
                'password': user_password,
                'scope': scope,
            },
            auth=(client_id, client_secret),
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        response.raise_for_status()
        data = response.json()
        try:
            expires_at = data['expires_in'] + int(time.time())
            return data['access_token'], datetime.datetime.utcfromtimestamp(expires_at)
        except KeyError:
            raise requests.RequestException(response=response)