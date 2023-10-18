def delete_datasets(self, **kwargs):
        """Delete datasets.

        Parameters
        -----------
        kwargs : logging information
            Find items to delete, leave it empty to delete all log.

        """

        self._fill_project_info(kwargs)
        self.db.Dataset.delete_many(kwargs)
        logging.info("[Database] Delete Dataset SUCCESS")