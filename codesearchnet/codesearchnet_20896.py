def set_topic(self, topic):
        """ Set the room topic.

        Args:
            topic (str): Topic

        Returns:
            bool. Success
        """
        if not topic:
            topic = ''
        result = self._connection.put("room/%s" % self.id, {"room": {"topic": topic}})
        if result["success"]:
            self._load()

        return result["success"]