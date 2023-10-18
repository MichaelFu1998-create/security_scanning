def authed_get(self, url, response_code=200, headers={}, follow=False):
        """Does a django test client ``get`` against the given url after
        logging in the admin first.

        :param url:
            URL to fetch
        :param response_code:
            Expected response code from the URL fetch.  This value is
            asserted.  Defaults to 200
        :param headers:
            Optional dictionary of headers to send in the request
        :param follow:
            When True, the get call will follow any redirect requests.
            Defaults to False.
        :returns:
            Django testing ``Response`` object
        """
        if not self.authed:
            self.authorize()

        response = self.client.get(url, follow=follow, **headers)
        self.assertEqual(response_code, response.status_code)
        return response