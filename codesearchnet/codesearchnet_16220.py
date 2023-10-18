def _execute(self, command, data=None, unpack=True):
        """Private method to execute command with data.

        Args:
            command(Command): The defined command.
            data(dict): The uri variable and body.

        Returns:
            The unwrapped value field in the json response.
        """
        if not data:
            data = {}
        data.setdefault('element_id', self.element_id)
        return self._driver._execute(command, data, unpack)