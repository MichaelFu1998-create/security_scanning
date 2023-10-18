def stop(self):
        """
        Stops HDLC controller's threads.
        """

        if self.receiver != None:
            self.receiver.join()

        for s in self.senders.values():
            s.join()