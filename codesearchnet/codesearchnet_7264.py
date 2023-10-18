def participant_ids(self):
        """:class:`~hangups.user.UserID` of users involved (:class:`list`)."""
        return [user.UserID(chat_id=id_.chat_id, gaia_id=id_.gaia_id)
                for id_ in self._event.membership_change.participant_ids]