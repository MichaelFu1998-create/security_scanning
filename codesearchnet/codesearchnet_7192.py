def from_entity(entity, self_user_id):
        """Construct user from ``Entity`` message.

        Args:
            entity: ``Entity`` message.
            self_user_id (~hangups.user.UserID or None): The ID of the current
                user. If ``None``, assume ``entity`` is the current user.

        Returns:
            :class:`~hangups.user.User` object.
        """
        user_id = UserID(chat_id=entity.id.chat_id,
                         gaia_id=entity.id.gaia_id)
        return User(user_id, entity.properties.display_name,
                    entity.properties.first_name,
                    entity.properties.photo_url,
                    entity.properties.email,
                    (self_user_id == user_id) or (self_user_id is None))