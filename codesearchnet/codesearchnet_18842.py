def connect(self):
        """ Connects and logins to the server. """
        self._ftp.connect()
        self._ftp.login(user=self._username, passwd=self._passwd)