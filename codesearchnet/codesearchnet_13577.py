def __error_message(self,stanza):
        """Process an error message from a MUC room.

        :Parameters:
            - `stanza`: the stanza received.
        :Types:
            - `stanza`: `Message`

        :return: `True` if the message was properly recognized as directed to
            one of the managed rooms, `False` otherwise.
        :returntype: `bool`"""
        fr=stanza.get_from()
        key=fr.bare().as_unicode()
        rs=self.rooms.get(key)
        if not rs:
            return False
        rs.process_error_message(stanza)
        return True