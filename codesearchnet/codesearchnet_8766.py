def _call_post_with_user_override(self, sap_user_id, url, payload):
        """
        Make a post request with an auth token acquired for a specific user to a SuccessFactors endpoint.

        Args:
            sap_user_id (str): The user to use to retrieve an auth token.
            url (str): The url to post to.
            payload (str): The json encoded payload to post.
        """
        SAPSuccessFactorsEnterpriseCustomerConfiguration = apps.get_model(  # pylint: disable=invalid-name
            'sap_success_factors',
            'SAPSuccessFactorsEnterpriseCustomerConfiguration'
        )
        oauth_access_token, _ = SAPSuccessFactorsAPIClient.get_oauth_access_token(
            self.enterprise_configuration.sapsf_base_url,
            self.enterprise_configuration.key,
            self.enterprise_configuration.secret,
            self.enterprise_configuration.sapsf_company_id,
            sap_user_id,
            SAPSuccessFactorsEnterpriseCustomerConfiguration.USER_TYPE_USER
        )

        response = requests.post(
            url,
            data=payload,
            headers={
                'Authorization': 'Bearer {}'.format(oauth_access_token),
                'content-type': 'application/json'
            }
        )

        return response.status_code, response.text