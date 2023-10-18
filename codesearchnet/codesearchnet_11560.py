def receive_finished(self):
        """return a list of pairs of IDs and results of finished tasks.

        This method doesn't wait for tasks to finish. It returns IDs
        and results which have already finished.

        Returns
        -------
        list
            A list of pairs of IDs and results

        """
        if not self.isopen:
            logger = logging.getLogger(__name__)
            logger.warning('the drop box is not open')
            return
        return self.dropbox.poll()