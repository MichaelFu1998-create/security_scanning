def _post(self, url, data=None):
        """
        Handle authenticated POST requests

        :param url: The url for the endpoint including path parameters
        :type url: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:data:`none` or :py:class:`dict`
        :returns: The JSON output from the API or an error message
        """
        url = urljoin(self.base_url, url)
        try:
            r = self._make_request(**dict(
                method='POST',
                url=url,
                json=data,
                auth=self.auth,
                timeout=self.timeout,
                hooks=self.request_hooks,
                headers=self.request_headers
            ))
        except requests.exceptions.RequestException as e:
            raise e
        else:
            if r.status_code >= 400:
                # in case of a 500 error, the response might not be a JSON
                try:
                    error_data = r.json()
                except ValueError:
                    error_data = { "response": r }
                raise MailChimpError(error_data)
            if r.status_code == 204:
                return None
            return r.json()