def get_command_responses(self):
        """
        Get responses to commands sent
        """
        if not self.response_queue.empty():
            yield None
        while not self.response_queue.empty():
            line = self.response_queue.get()
            if line is not None:
                yield line