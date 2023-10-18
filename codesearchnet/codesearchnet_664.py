def save_validation_log(self, **kwargs):
        """Saves the validation log, timestamp will be added automatically.

        Parameters
        -----------
        kwargs : logging information
            Events, such as accuracy, loss, step number and etc.

        Examples
        ---------
        >>> db.save_validation_log(accuracy=0.33, loss=0.98)

        """

        self._fill_project_info(kwargs)
        kwargs.update({'time': datetime.utcnow()})
        _result = self.db.ValidLog.insert_one(kwargs)
        _log = self._print_dict(kwargs)
        logging.info("[Database] valid log: " + _log)