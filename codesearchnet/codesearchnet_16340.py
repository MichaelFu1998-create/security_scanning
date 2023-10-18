def send(self, data):
        """
        Sends a new data frame.

        This method will block until a new room is available for
        a new sender. This limit is determined by the size of the window.
        """

        while len(self.senders) >= self.window:
            pass

        self.senders[self.new_seq_no] = self.Sender(
            self.write,
            self.send_lock,
            data,
            self.new_seq_no,
            timeout=self.sending_timeout,
            callback=self.send_callback,
        )

        self.senders[self.new_seq_no].start()
        self.new_seq_no = (self.new_seq_no + 1) % HDLController.MAX_SEQ_NO