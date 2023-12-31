def __presence_unavailable(self,stanza):
        """Process an unavailable presence from a MUC room.

        :Parameters:
            - `stanza`: the stanza received.
        :Types:
            - `stanza`: `Presence`

        :return: `True` if the stanza was properly recognized as generated by
            one of the managed rooms, `False` otherwise.
        :returntype: `bool`"""
        fr=stanza.get_from()
        key=fr.bare().as_unicode()
        rs=self.rooms.get(key)
        if not rs:
            return False
        rs.process_unavailable_presence(MucPresence(stanza))
        return True