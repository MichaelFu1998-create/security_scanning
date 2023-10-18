def stop(self) -> float:
        """
        Stop the timer

        Returns:
            The time the timer was stopped
        """
        self.stop_time = time.time()
        return self.stop_time - self.start_time - self.offset