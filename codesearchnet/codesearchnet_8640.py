def _delete(self, url, data, scope):
        """
        Make a DELETE request using the session object to a Degreed endpoint.

        Args:
            url (str): The url to send a DELETE request to.
            data (str): The json encoded payload to DELETE.
            scope (str): Must be one of the scopes Degreed expects:
                        - `CONTENT_PROVIDER_SCOPE`
                        - `COMPLETION_PROVIDER_SCOPE`
        """
        self._create_session(scope)
        response = self.session.delete(url, data=data)
        return response.status_code, response.text