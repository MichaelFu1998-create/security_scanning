def check_nonce(self, request, oauth_request):
        """
        Checks nonce of request, and return True if valid.
        """
        oauth_nonce = oauth_request['oauth_nonce']
        oauth_timestamp = oauth_request['oauth_timestamp']
        return check_nonce(request, oauth_request, oauth_nonce, oauth_timestamp)