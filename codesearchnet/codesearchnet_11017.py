def get_time(self) -> float:
        """
        Get the current time in seconds

        Returns:
            The current time in seconds
        """
        if self.pause_time is not None:
            curr_time = self.pause_time - self.offset - self.start_time
            return curr_time

        curr_time = time.time()
        return curr_time - self.start_time - self.offset