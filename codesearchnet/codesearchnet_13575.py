def forget(self,rs):
        """
        Remove a room from the list of managed rooms.

        :Parameters:
            - `rs`: the state object of the room.
        :Types:
            - `rs`: `MucRoomState`
        """
        try:
            del self.rooms[rs.room_jid.bare().as_unicode()]
        except KeyError:
            pass