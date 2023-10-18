def delete_tasks(self, **kwargs):
        """Delete tasks.

        Parameters
        -----------
        kwargs : logging information
            Find items to delete, leave it empty to delete all log.

        Examples
        ---------
        >>> db.delete_tasks()

        """

        self._fill_project_info(kwargs)
        self.db.Task.delete_many(kwargs)
        logging.info("[Database] Delete Task SUCCESS")