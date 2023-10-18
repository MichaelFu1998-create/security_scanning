def get_user(self, user_id):
        """
        Get a user by their ID.

        Args:
            user_id:
                The ID of the user to fetch.

        Returns:
            The user with the specified ID if they exist and ``None``
            otherwise.
        """
        try:
            return get_user_model().objects.get(id=user_id)
        except get_user_model().DoesNotExist:
            return None