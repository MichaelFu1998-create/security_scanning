def logon(self, username, password):
        """
        Logs the user on to FogBugz.

        Returns None for a successful login.
        """
        if self._token:
            self.logoff()
        try:
            response = self.__makerequest(
                'logon', email=username, password=password)
        except FogBugzAPIError:
            e = sys.exc_info()[1]
            raise FogBugzLogonError(e)

        self._token = response.token.string
        if type(self._token) == CData:
                self._token = self._token.encode('utf-8')