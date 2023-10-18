def leave(self):
        """
        Send a leave request for the room.
        """
        if self.joined:
            p=MucPresence(to_jid=self.room_jid,stanza_type="unavailable")
            self.manager.stream.send(p)