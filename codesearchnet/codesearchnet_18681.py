def request(self, url, method="GET", data=None, params=None, retry=True):
        """
        Make a request to the NuHeat API

        :param url: The URL to request
        :param method: The type of request to make (GET, POST)
        :param data: Data to be sent along with POST requests
        :param params: Querystring parameters
        :param retry: Attempt to re-authenticate and retry request if necessary
        """
        headers = config.REQUEST_HEADERS

        if params and self._session_id:
            params['sessionid'] = self._session_id

        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, params=params, data=data)

        # Handle expired sessions
        if response.status_code == 401 and retry:
            _LOGGER.warn("NuHeat APIrequest unauthorized [401]. Try to re-authenticate.")
            self._session_id = None
            self.authenticate()
            return self.request(url, method=method, data=data, params=params, retry=False)

        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            # No JSON object
            return response