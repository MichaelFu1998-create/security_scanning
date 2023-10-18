def join(self, room, nick, handler, password = None, history_maxchars = None,
            history_maxstanzas = None, history_seconds = None, history_since = None):
        """
        Create and return a new room state object and request joining
        to a MUC room.

        :Parameters:
            - `room`: the name of a room to be joined
            - `nick`: the nickname to be used in the room
            - `handler`: is an object to handle room events.
            - `password`: password for the room, if any
            - `history_maxchars`: limit of the total number of characters in
              history.
            - `history_maxstanzas`: limit of the total number of messages in
              history.
            - `history_seconds`: send only messages received in the last
              `history_seconds` seconds.
            - `history_since`: Send only the messages received since the
              dateTime specified (UTC).

        :Types:
            - `room`: `JID`
            - `nick`: `unicode`
            - `handler`: `MucRoomHandler`
            - `password`: `unicode`
            - `history_maxchars`: `int`
            - `history_maxstanzas`: `int`
            - `history_seconds`: `int`
            - `history_since`: `datetime.datetime`

        :return: the room state object created.
        :returntype: `MucRoomState`
        """

        if not room.node or room.resource:
            raise ValueError("Invalid room JID")

        room_jid = JID(room.node, room.domain, nick)

        cur_rs = self.rooms.get(room_jid.bare().as_unicode())
        if cur_rs and cur_rs.joined:
            raise RuntimeError("Room already joined")

        rs=MucRoomState(self, self.stream.me, room_jid, handler)
        self.rooms[room_jid.bare().as_unicode()]=rs
        rs.join(password, history_maxchars, history_maxstanzas,
            history_seconds, history_since)
        return rs