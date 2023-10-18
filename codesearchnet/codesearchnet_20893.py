def get_users(self, sort=True):
        """ Get list of users in the room.

        Kwargs:
            sort (bool): If True, sort rooms by name

        Returns:
            array. List of users
        """
        self._load()
        if sort:
            self.users.sort(key=operator.itemgetter("name"))
        return self.users