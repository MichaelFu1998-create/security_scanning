def set_subject(self,subject):
        """
        Send a subject change request to the room.

        :Parameters:
            - `subject`: the new subject.
        :Types:
            - `subject`: `unicode`
        """
        m=Message(to_jid=self.room_jid.bare(),stanza_type="groupchat",subject=subject)
        self.manager.stream.send(m)