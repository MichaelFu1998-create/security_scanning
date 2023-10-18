def delete_training_log(self, **kwargs):
        """Deletes training log.

        Parameters
        -----------
        kwargs : logging information
            Find items to delete, leave it empty to delete all log.

        Examples
        ---------
        Save training log
        >>> db.save_training_log(accuracy=0.33)
        >>> db.save_training_log(accuracy=0.44)

        Delete logs that match the requirement
        >>> db.delete_training_log(accuracy=0.33)

        Delete all logs
        >>> db.delete_training_log()
        """
        self._fill_project_info(kwargs)
        self.db.TrainLog.delete_many(kwargs)
        logging.info("[Database] Delete TrainLog SUCCESS")