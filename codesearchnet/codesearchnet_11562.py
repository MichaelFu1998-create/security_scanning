def receive_all(self):
        """return a list of pairs of IDs and results of all tasks.

        This method waits for all tasks to finish.

        Returns
        -------
        list
            A list of pairs of IDs and results

        """
        if not self.isopen:
            logger = logging.getLogger(__name__)
            logger.warning('the drop box is not open')
            return
        return self.dropbox.receive()