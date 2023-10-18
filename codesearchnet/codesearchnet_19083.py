def refresh_access_token(self,):
        """Refresh access token
        """
        logger.debug("REFRESHING TOKEN")
        self.token_time = time.time()
        credentials = {
            'token_time': self.token_time
        }

        if self.oauth_version == 'oauth1':
            self.access_token, self.access_token_secret = self.oauth.get_access_token(self.access_token, self.access_token_secret, params={"oauth_session_handle": self.session_handle})
            credentials.update({
                'access_token': self.access_token,
                'access_token_secret': self.access_token_secret,
                'session_handle': self.session_handle,
                'token_time': self.token_time
            })
        else:
            headers = self.generate_oauth2_headers()

            raw_access = self.oauth.get_raw_access_token(data={"refresh_token": self.refresh_token, 'redirect_uri': self.callback_uri,'grant_type':'refresh_token'}, headers=headers)
            credentials.update(self.oauth2_access_parser(raw_access))            

        return credentials