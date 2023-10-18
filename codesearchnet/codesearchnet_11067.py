def get_time(self) -> float:
        """
        Get the current time in seconds

        Returns:
            The current time in seconds
        """
        if self.paused:
            return self.pause_time

        return self.player.get_time() / 1000.0