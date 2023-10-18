def get_oauth_access_token(url_base, client_id, client_secret, company_id, user_id, user_type):
        """ Retrieves OAuth 2.0 access token using the client credentials grant.

        Args:
            url_base (str): Oauth2 access token endpoint
            client_id (str): client ID
            client_secret (str): client secret
            company_id (str): SAP company ID
            user_id (str): SAP user ID
            user_type (str): type of SAP user (admin or user)

        Returns:
            tuple: Tuple containing access token string and expiration datetime.
        Raises:
            HTTPError: If we received a failure response code from SAP SuccessFactors.
            RequestException: If an unexpected response format was received that we could not parse.
        """
        SAPSuccessFactorsGlobalConfiguration = apps.get_model(  # pylint: disable=invalid-name
            'sap_success_factors',
            'SAPSuccessFactorsGlobalConfiguration'
        )
        global_sap_config = SAPSuccessFactorsGlobalConfiguration.current()
        url = url_base + global_sap_config.oauth_api_path

        response = requests.post(
            url,
            json={
                'grant_type': 'client_credentials',
                'scope': {
                    'userId': user_id,
                    'companyId': company_id,
                    'userType': user_type,
                    'resourceType': 'learning_public_api',
                }
            },
            auth=(client_id, client_secret),
            headers={'content-type': 'application/json'}
        )

        response.raise_for_status()
        data = response.json()
        try:
            return data['access_token'], datetime.datetime.utcfromtimestamp(data['expires_in'] + int(time.time()))
        except KeyError:
            raise requests.RequestException(response=response)