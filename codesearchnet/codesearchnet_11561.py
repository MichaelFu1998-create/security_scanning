def receive_one(self):
        """return a pair of an ID and a result of a task.

        This method waits for a task to finish.

        Returns
        -------
        An ID and a result of a task. `None` if no task is running.

        """
        if not self.isopen:
            logger = logging.getLogger(__name__)
            logger.warning('the drop box is not open')
            return
        return self.dropbox.receive_one()