def speak(self, message):
        """ Post a message.

        Args:
            message (:class:`Message` or string): Message

        Returns:
            bool. Success
        """
        campfire = self.get_campfire()
        if not isinstance(message, Message):
            message = Message(campfire, message)

        result = self._connection.post(
            "room/%s/speak" % self.id,
            {"message": message.get_data()},
            parse_data=True,
            key="message"
        )

        if result["success"]:
            return Message(campfire, result["data"])
        return result["success"]