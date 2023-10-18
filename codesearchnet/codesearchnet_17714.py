def _authenticate(self):
        """
        Authenticate with the API and return an authentication token.
        """
        auth_url = BASE_URL + "/auth/token"
        payload = {'username': self.email, 'password': self.password, 'grant_type': 'password'}
        arequest = requests.post(auth_url, data=payload, headers=BASIC_HEADERS)
        status = arequest.status_code
        if status != 200:
            _LOGGER.error("Authentication request failed, please check credintials. " + str(status))
            return False
        response = arequest.json()
        _LOGGER.debug(str(response))
        self.token = response.get("access_token")
        self.refresh_token = response.get("refresh_token")
        _auth = HEADERS.get("Authorization")
        _auth = _auth % self.token
        HEADERS["Authorization"] = _auth
        _LOGGER.info("Authentication was successful, token set.")
        return True