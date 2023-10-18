def messages(self):
        """Return active messages."""
        method = 'GET'
        url = 'activeMessage'

        rc = self.__request__(method, url)
        # try:
        #     return rc['activeMessage']
        # except:
        #     raise UnknownError('Invalid activeMessage response')  # is it even possible?
        return rc['activeMessage']