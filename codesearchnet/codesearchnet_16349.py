def validate_token(self, request, consumer, token):
        """
        Check the token and raise an `oauth.Error` exception if invalid.
        """
        oauth_server, oauth_request = oauth_provider.utils.initialize_server_request(request)
        oauth_server.verify_request(oauth_request, consumer, token)