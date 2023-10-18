def set_time(self, value: float):
        """
        Set the current time jumping in the timeline.

        Args:
            value (float): The new time
        """
        if value < 0:
            value = 0

        self.controller.row = self.rps * value