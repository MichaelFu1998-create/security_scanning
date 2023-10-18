def _create_session(self):
        """
        Instantiate a new session object for use in connecting with SAP SuccessFactors
        """
        session = requests.Session()
        session.timeout = self.SESSION_TIMEOUT

        oauth_access_token, expires_at = SAPSuccessFactorsAPIClient.get_oauth_access_token(
            self.enterprise_configuration.sapsf_base_url,
            self.enterprise_configuration.key,
            self.enterprise_configuration.secret,
            self.enterprise_configuration.sapsf_company_id,
            self.enterprise_configuration.sapsf_user_id,
            self.enterprise_configuration.user_type
        )

        session.headers['Authorization'] = 'Bearer {}'.format(oauth_access_token)
        session.headers['content-type'] = 'application/json'
        self.session = session
        self.expires_at = expires_at