def exchange_token(self, code):
        """
        Exchange the authorization code for an access token.
        """
        access_token_url = OAUTH_ROOT + '/access_token'
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code': code,
        }
        resp = requests.get(access_token_url, params=params)
        if not resp.ok:
            raise MixcloudOauthError("Could not get access token.")
        return resp.json()['access_token']