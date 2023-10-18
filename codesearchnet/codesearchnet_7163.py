def users(self):
        """List of conversation participants (:class:`~hangups.user.User`)."""
        return [self._user_list.get_user(user.UserID(chat_id=part.id.chat_id,
                                                     gaia_id=part.id.gaia_id))
                for part in self._conversation.participant_data]