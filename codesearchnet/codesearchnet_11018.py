def set_time(self, value: float):
        """
        Set the current time. This can be used to jump in the timeline.

        Args:
            value (float): The new time
        """
        if value < 0:
            value = 0

        self.offset += self.get_time() - value