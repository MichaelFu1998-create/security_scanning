def send_message(self):
        """Send message over UDP.

        If tracking is disables, the bytes_sent will always be set to -1

        Returns:
            (bytes_sent, time_taken)
        """
        start = time.time()
        message = None
        if not self.initialized:
            message = self.construct_start_message()
            self.initialized = True
        else:
            message = self.construct_end_message()

        self.send_UDP_message(message)
        end = time.time()

        return end - start