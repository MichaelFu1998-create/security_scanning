def poll(self):
        """Return pairs of run ids and results of finish event loops.
        """
        ret = self.communicationChannel.receive_finished()
        self.nruns -= len(ret)
        return ret