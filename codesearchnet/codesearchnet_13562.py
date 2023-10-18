def change_nick(self,new_nick):
        """
        Send a nick change request to the room.

        :Parameters:
            - `new_nick`: the new nickname requested.
        :Types:
            - `new_nick`: `unicode`
        """
        new_room_jid=JID(self.room_jid.node,self.room_jid.domain,new_nick)
        p=Presence(to_jid=new_room_jid)
        self.manager.stream.send(p)