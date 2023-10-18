def set(self, user):
        """
        Adds a user object to the user manager

        user - a SlackUser object
        """

        self.log.info("Loading user information for %s/%s", user.id, user.username)
        self.load_user_info(user)
        self.log.info("Loading user rights for %s/%s", user.id, user.username)
        self.load_user_rights(user)
        self.log.info("Added user: %s/%s", user.id, user.username)
        self._add_user_to_cache(user)
        return user