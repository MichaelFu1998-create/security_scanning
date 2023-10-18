def get_user(self, user_id):
        """Get a user by its ID.

        Args:
            user_id (~hangups.user.UserID): The ID of the user.

        Raises:
            KeyError: If no such user is known.

        Returns:
            :class:`~hangups.user.User` with the given ID.
        """
        try:
            return self._user_dict[user_id]
        except KeyError:
            logger.warning('UserList returning unknown User for UserID %s',
                           user_id)
            return User(user_id, None, None, None, [], False)