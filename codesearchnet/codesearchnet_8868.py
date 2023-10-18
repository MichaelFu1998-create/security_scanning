def _login(self, email, password):
        """
        Login to pybotvac account using provided email and password.

        :param email: email for pybotvac account
        :param password: Password for pybotvac account
        :return:
        """
        response = requests.post(urljoin(self.ENDPOINT, 'sessions'),
                                 json={'email': email,
                                       'password': password,
                                       'platform': 'ios',
                                       'token': binascii.hexlify(os.urandom(64)).decode('utf8')},
                                 headers=self._headers)

        response.raise_for_status()
        access_token = response.json()['access_token']

        self._headers['Authorization'] = 'Token token=%s' % access_token