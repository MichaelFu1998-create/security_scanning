def start(self):
        """
        Starts HDLC controller's threads.
        """

        self.receiver = self.Receiver(
            self.read,
            self.write,
            self.send_lock,
            self.senders,
            self.frames_received,
            callback=self.receive_callback,
            fcs_nack=self.fcs_nack,
        )

        self.receiver.start()