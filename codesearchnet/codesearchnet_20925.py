def get_room_by_name(self, name):
        """ Get a room by name.

        Returns:
            :class:`Room`. Room

        Raises:
            RoomNotFoundException
        """
        rooms = self.get_rooms()
        for room in rooms or []:
            if room["name"] == name:
                return self.get_room(room["id"])
        raise RoomNotFoundException("Room %s not found" % name)