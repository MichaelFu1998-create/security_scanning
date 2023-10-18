def set_name(self, name):
        """ Set the room name.

        Args:
            name (str): Name

        Returns:
            bool. Success
        """
        if not self._campfire.get_user().admin:
            return False

        result = self._connection.put("room/%s" % self.id, {"room": {"name": name}})
        if result["success"]:
            self._load()
        return result["success"]