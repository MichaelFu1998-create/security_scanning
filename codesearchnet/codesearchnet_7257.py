def user_id(self):
        """Who created the event (:class:`~hangups.user.UserID`)."""
        return user.UserID(chat_id=self._event.sender_id.chat_id,
                           gaia_id=self._event.sender_id.gaia_id)