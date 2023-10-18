def authed_post(self, url, data, response_code=200, follow=False,
            headers={}):
        """Does a django test client ``post`` against the given url after
        logging in the admin first.

        :param url:
            URL to fetch
        :param data:
            Dictionary to form contents to post
        :param response_code:
            Expected response code from the URL fetch.  This value is
            asserted.  Defaults to 200
        :param headers:
            Optional dictionary of headers to send in with the request
        :returns:
            Django testing ``Response`` object
        """
        if not self.authed:
            self.authorize()

        response = self.client.post(url, data, follow=follow, **headers)
        self.assertEqual(response_code, response.status_code)
        return response