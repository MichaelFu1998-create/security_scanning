def handler(self,):
        """* get request token if OAuth1
            * Get user authorization
            * Get access token
        """

        if self.oauth_version == 'oauth1':
            request_token, request_token_secret = self.oauth.get_request_token(params={'oauth_callback': self.callback_uri})
            logger.debug("REQUEST_TOKEN = {0}\n REQUEST_TOKEN_SECRET = {1}\n".format(request_token, request_token_secret))
            authorize_url = self.oauth.get_authorize_url(request_token)
        else:
            authorize_url = self.oauth.get_authorize_url(client_secret=self.consumer_secret, redirect_uri=self.callback_uri, response_type='code')

        logger.debug("AUTHORISATION URL : {0}".format(authorize_url))
        # Open authorize_url
        webbrowser.open(authorize_url)
        self.verifier = input("Enter verifier : ")

        self.token_time = time.time()
    
        credentials = {'token_time': self.token_time}
        
        if self.oauth_version == 'oauth1':
            raw_access = self.oauth.get_raw_access_token(request_token, request_token_secret, params={"oauth_verifier": self.verifier})
            parsed_access = parse_utf8_qsl(raw_access.content)
            self.access_token = parsed_access['oauth_token']
            self.access_token_secret = parsed_access['oauth_token_secret']
            self.session_handle = parsed_access['oauth_session_handle']
            self.guid = parsed_access['xoauth_yahoo_guid']
            
            # Updating credentials 
            credentials.update({
                'access_token': self.access_token,
                'access_token_secret': self.access_token_secret,
                'session_handle': self.session_handle,
                'guid': self.guid
            })
        else:
            # Building headers 
            headers = self.generate_oauth2_headers()
            # Getting access token
            raw_access = self.oauth.get_raw_access_token(data={"code": self.verifier, 'redirect_uri': self.callback_uri,'grant_type':'authorization_code'}, headers=headers)
            #parsed_access = parse_utf8_qsl(raw_access.content.decode('utf-8'))
            credentials.update(self.oauth2_access_parser(raw_access))
                    
        return credentials