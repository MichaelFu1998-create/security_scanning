def stopProducing(self):
        """ Stop producing """
        self._finish(True)
        if self._deferred and self._sent < self.length:
            self._deferred.errback(Exception("Consumer asked to stop production of request body (%d sent out of %d)" % (self._sent, self.length)))