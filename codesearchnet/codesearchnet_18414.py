def authorize_url(self):
        """
        Return a URL to redirect the user to for OAuth authentication.
        """
        auth_url = OAUTH_ROOT + '/authorize'
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
        }
        return "{}?{}".format(auth_url, urlencode(params))