def assume_localhost(self):
        """
        Sets connection parameters to localhost, if not set already.
        """
        if not self.genv.host_string:
            self.genv.host_string = 'localhost'
            self.genv.hosts = ['localhost']
            self.genv.user = getpass.getuser()