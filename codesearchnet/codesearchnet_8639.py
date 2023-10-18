def _post(self, url, data, scope):
        """
        Make a POST request using the session object to a Degreed endpoint.

        Args:
            url (str): The url to send a POST request to.
            data (str): The json encoded payload to POST.
            scope (str): Must be one of the scopes Degreed expects:
                        - `CONTENT_PROVIDER_SCOPE`
                        - `COMPLETION_PROVIDER_SCOPE`
        """
        self._create_session(scope)
        response = self.session.post(url, data=data)
        return response.status_code, response.text