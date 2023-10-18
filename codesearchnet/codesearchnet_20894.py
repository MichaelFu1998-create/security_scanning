def recent(self, message_id=None, limit=None):
        """ Recent messages.

        Kwargs:
            message_id (int): If specified, return messages since the specified message ID
            limit (int): If specified, limit the number of messages

        Returns:
            array. Messages
        """
        parameters = {}
        if message_id:
            parameters["since_message_id"] = message_id
        if limit:
            parameters["limit"] = limit
        messages = self._connection.get("room/%s/recent" % self.id, key="messages", parameters=parameters)
        if messages:
            messages = [Message(self._campfire, message) for message in messages]
        return messages