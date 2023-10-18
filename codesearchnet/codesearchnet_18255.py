def get_user(self, username):
        """
        Utility function to query slack for a particular user

        :param username: The username of the user to lookup
        :return: SlackUser object or None
        """
        if hasattr(self._bot, 'user_manager'):
            user = self._bot.user_manager.get_by_username(username)
            if user:
                return user
            user = SlackUser.get_user(self._bot.sc, username)
            self._bot.user_manager.set(user)
            return user
        return SlackUser.get_user(self._bot.sc, username)