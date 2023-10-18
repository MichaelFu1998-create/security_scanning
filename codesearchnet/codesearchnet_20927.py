def get_user(self, id = None):
        """ Get user.

        Returns:
            :class:`User`. User
        """
        if not id:
            id = self._user.id

        if id not in self._users:
            self._users[id] = self._user if id == self._user.id else User(self, id)

        return self._users[id]