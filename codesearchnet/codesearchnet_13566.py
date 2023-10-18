def process_groupchat_message(self,stanza):
        """
        Process <message type="groupchat"/> received from the room.

        :Parameters:
            - `stanza`: the stanza received.
        :Types:
            - `stanza`: `Message`
        """
        fr=stanza.get_from()
        user=self.get_user(fr,True)
        s=stanza.get_subject()
        if s:
            self.subject=s
            self.handler.subject_changed(user,stanza)
        else:
            self.handler.message_received(user,stanza)