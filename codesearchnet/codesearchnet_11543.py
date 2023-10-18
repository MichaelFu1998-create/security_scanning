def end(self):
        """wait until all event loops end and returns the results.

        """

        results = self.communicationChannel.receive()

        if self.nruns != len(results):
            import logging
            logger = logging.getLogger(__name__)
            # logger.setLevel(logging.DEBUG)
            logger.warning(
                'too few results received: {} results received, {} expected'.format(
                    len(results),
                    self.nruns
                ))

        return results