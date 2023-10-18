def receive_one(self):
        """Return a pair of a run id and a result.

        This method waits until an event loop finishes.
        This method returns None if no loop is running.
        """
        if self.nruns == 0:
            return None
        ret = self.communicationChannel.receive_one()
        if ret is not None:
            self.nruns -= 1
        return ret