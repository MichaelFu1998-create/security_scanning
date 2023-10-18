def delete_validation_log(self, **kwargs):
        """Deletes validation log.

        Parameters
        -----------
        kwargs : logging information
            Find items to delete, leave it empty to delete all log.

        Examples
        ---------
        - see ``save_training_log``.
        """
        self._fill_project_info(kwargs)
        self.db.ValidLog.delete_many(kwargs)
        logging.info("[Database] Delete ValidLog SUCCESS")