def _call_post_with_session(self, url, payload):
        """
        Make a post request using the session object to a SuccessFactors endpoint.

        Args:
            url (str): The url to post to.
            payload (str): The json encoded payload to post.
        """
        now = datetime.datetime.utcnow()
        if now >= self.expires_at:
            # Create a new session with a valid token
            self.session.close()
            self._create_session()
        response = self.session.post(url, data=payload)
        return response.status_code, response.text