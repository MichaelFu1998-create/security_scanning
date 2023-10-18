def get_user(self,nick_or_jid,create=False):
        """
        Get a room user with given nick or JID.

        :Parameters:
            - `nick_or_jid`: the nickname or room JID of the user requested.
            - `create`: if `True` and `nick_or_jid` is a JID, then a new
              user object will be created if there is no such user in the room.
        :Types:
            - `nick_or_jid`: `unicode` or `JID`
            - `create`: `bool`

        :return: the named user or `None`
        :returntype: `MucRoomUser`
        """
        if isinstance(nick_or_jid,JID):
            if not nick_or_jid.resource:
                return None
            for u in self.users.values():
                if nick_or_jid in (u.room_jid,u.real_jid):
                    return u
            if create:
                return MucRoomUser(nick_or_jid)
            else:
                return None
        return self.users.get(nick_or_jid)