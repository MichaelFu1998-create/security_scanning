def get_room_jid(self,nick=None):
        """
        Get own room JID or a room JID for given `nick`.

        :Parameters:
            - `nick`: a nick for which the room JID is requested.
        :Types:
            - `nick`: `unicode`

        :return: the room JID.
        :returntype: `JID`
        """
        if nick is None:
            return self.room_jid
        return JID(self.room_jid.node,self.room_jid.domain,nick)