def incoming(self, messages):
        """ Called when incoming messages arrive.

        Args:
            messages (tuple): Messages (each message is a dict)
        """
        if self._observers:
            campfire = self._room.get_campfire()
            for message in messages:
                for observer in self._observers:
                    observer(Message(campfire, message))