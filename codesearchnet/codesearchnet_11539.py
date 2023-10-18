def run_multiple(self, eventLoops):
        """run the event loops in the background.

        Args:
            eventLoops (list): a list of event loops to run

        """

        self.nruns += len(eventLoops)
        return self.communicationChannel.put_multiple(eventLoops)