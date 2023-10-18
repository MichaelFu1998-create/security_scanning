def receive(self):
        """Return pairs of run ids and results.

        This method waits until all event loops finish
        """
        ret = self.communicationChannel.receive_all()
        self.nruns -= len(ret)
        if self.nruns > 0:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(
                'too few results received: {} results received, {} more expected'.format(
                    len(ret), self.nruns))
        elif self.nruns < 0:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(
                'too many results received: {} results received, {} too many'.format(
                    len(ret), -self.nruns))
        return ret