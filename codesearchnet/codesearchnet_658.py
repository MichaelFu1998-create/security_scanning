def delete_model(self, **kwargs):
        """Delete model.

        Parameters
        -----------
        kwargs : logging information
            Find items to delete, leave it empty to delete all log.
        """
        self._fill_project_info(kwargs)
        self.db.Model.delete_many(kwargs)
        logging.info("[Database] Delete Model SUCCESS")