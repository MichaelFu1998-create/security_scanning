def resumeProducing(self):
        """ Resume producing """
        self._paused = False
        result = self._produce()
        if result:
            return result