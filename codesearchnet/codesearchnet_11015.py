def start(self):
        """
        Start the timer by recoding the current ``time.time()``
        preparing to report the number of seconds since this timestamp.
        """
        if self.start_time is None:
            self.start_time = time.time()
        # Play after pause
        else:
            # Add the duration of the paused interval to the total offset
            pause_duration = time.time() - self.pause_time
            self.offset += pause_duration
            # print("pause duration", pause_duration, "offset", self.offset)
            # Exit the paused state
            self.pause_time = None