def set_login(self, callsign, passwd="-1", skip_login=False):
        """
        Set callsign and password
        """
        self.__dict__.update(locals())