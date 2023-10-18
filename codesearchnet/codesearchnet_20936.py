def fetch(self):
        """ Fetch new messages. """
        try:
            if not self._last_message_id:
                messages = self._connection.get("room/%s/recent" % self._room_id, key="messages", parameters={
                    "limit": 1
                })
                self._last_message_id = messages[-1]["id"]

            messages = self._connection.get("room/%s/recent" % self._room_id, key="messages", parameters={
                "since_message_id": self._last_message_id
            })
        except:
            messages = []

        if messages:
            self._last_message_id = messages[-1]["id"]

        self.received(messages)