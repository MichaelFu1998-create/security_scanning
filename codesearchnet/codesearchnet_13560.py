def send_message(self,body):
        """
        Send a message to the room.

        :Parameters:
            - `body`: the message body.
        :Types:
            - `body`: `unicode`
        """
        m=Message(to_jid=self.room_jid.bare(),stanza_type="groupchat",body=body)
        self.manager.stream.send(m)