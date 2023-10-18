def store(self, key: object, value: object):
        """ Stores custom user data. """
        self._user_data.update({key: value})