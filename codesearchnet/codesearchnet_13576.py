def __groupchat_message(self,stanza):
        """Process a groupchat message from a MUC room.

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
            self.__logger.debug("groupchat message from unknown source")
            return False
        rs.process_groupchat_message(stanza)
        return True