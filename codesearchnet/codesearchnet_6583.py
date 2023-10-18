def clubStaff(self):
        """Return staff in your club."""
        method = 'GET'
        url = 'club/stats/staff'

        rc = self.__request__(method, url)
        return rc