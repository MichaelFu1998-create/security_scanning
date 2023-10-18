def get_rooms(self, sort=True):
        """ Get rooms list.

        Kwargs:
            sort (bool): If True, sort rooms by name

        Returns:
            array. List of rooms (each room is a dict)
        """
        rooms = self._connection.get("rooms")
        if sort:
            rooms.sort(key=operator.itemgetter("name"))
        return rooms