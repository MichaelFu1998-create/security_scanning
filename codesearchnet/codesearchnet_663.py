def save_training_log(self, **kwargs):
        """Saves the training log, timestamp will be added automatically.

        Parameters
        -----------
        kwargs : logging information
            Events, such as accuracy, loss, step number and etc.

        Examples
        ---------
        >>> db.save_training_log(accuracy=0.33, loss=0.98)

        """

        self._fill_project_info(kwargs)
        kwargs.update({'time': datetime.utcnow()})
        _result = self.db.TrainLog.insert_one(kwargs)
        _log = self._print_dict(kwargs)
        logging.info("[Database] train log: " + _log)