def save_dataset(self, dataset=None, dataset_name=None, **kwargs):
        """Saves one dataset into database, timestamp will be added automatically.

        Parameters
        ----------
        dataset : any type
            The dataset you want to store.
        dataset_name : str
            The name of dataset.
        kwargs : other events
            Other events, such as description, author and etc (optinal).

        Examples
        ----------
        Save dataset
        >>> db.save_dataset([X_train, y_train, X_test, y_test], 'mnist', description='this is a tutorial')

        Get dataset
        >>> dataset = db.find_top_dataset('mnist')

        Returns
        ---------
        boolean : Return True if save success, otherwise, return False.
        """
        self._fill_project_info(kwargs)
        if dataset_name is None:
            raise Exception("dataset_name is None, please give a dataset name")
        kwargs.update({'dataset_name': dataset_name})

        s = time.time()
        try:
            dataset_id = self.dataset_fs.put(self._serialization(dataset))
            kwargs.update({'dataset_id': dataset_id, 'time': datetime.utcnow()})
            self.db.Dataset.insert_one(kwargs)
            # print("[Database] Save params: {} SUCCESS, took: {}s".format(file_name, round(time.time()-s, 2)))
            print("[Database] Save dataset: SUCCESS, took: {}s".format(round(time.time() - s, 2)))
            return True
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.info("{}  {}  {}  {}  {}".format(exc_type, exc_obj, fname, exc_tb.tb_lineno, e))
            print("[Database] Save dataset: FAIL")
            return False