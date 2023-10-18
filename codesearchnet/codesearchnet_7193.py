def from_conv_part_data(conv_part_data, self_user_id):
        """Construct user from ``ConversationParticipantData`` message.

        Args:
            conv_part_id: ``ConversationParticipantData`` message.
            self_user_id (~hangups.user.UserID or None): The ID of the current
                user. If ``None``, assume ``conv_part_id`` is the current user.

        Returns:
            :class:`~hangups.user.User` object.
        """
        user_id = UserID(chat_id=conv_part_data.id.chat_id,
                         gaia_id=conv_part_data.id.gaia_id)
        return User(user_id, conv_part_data.fallback_name, None, None, [],
                    (self_user_id == user_id) or (self_user_id is None))