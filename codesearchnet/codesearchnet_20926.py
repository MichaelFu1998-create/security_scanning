def get_room(self, id):
        """ Get room.

        Returns:
            :class:`Room`. Room
        """
        if id not in self._rooms:
            self._rooms[id] = Room(self, id)
        return self._rooms[id]