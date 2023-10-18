def find_top_dataset(self, dataset_name=None, sort=None, **kwargs):
        """Finds and returns a dataset from the database which matches the requirement.

        Parameters
        ----------
        dataset_name : str
            The name of dataset.
        sort : List of tuple
            PyMongo sort comment, search "PyMongo find one sorting" and `collection level operations <http://api.mongodb.com/python/current/api/pymongo/collection.html>`__ for more details.
        kwargs : other events
            Other events, such as description, author and etc (optinal).

        Examples
        ---------
        Save dataset
        >>> db.save_dataset([X_train, y_train, X_test, y_test], 'mnist', description='this is a tutorial')

        Get dataset
        >>> dataset = db.find_top_dataset('mnist')
        >>> datasets = db.find_datasets('mnist')

        Returns
        --------
        dataset : the dataset or False
            Return False if nothing found.

        """

        self._fill_project_info(kwargs)
        if dataset_name is None:
            raise Exception("dataset_name is None, please give a dataset name")
        kwargs.update({'dataset_name': dataset_name})

        s = time.time()

        d = self.db.Dataset.find_one(filter=kwargs, sort=sort)

        if d is not None:
            dataset_id = d['dataset_id']
        else:
            print("[Database] FAIL! Cannot find dataset: {}".format(kwargs))
            return False
        try:
            dataset = self._deserialization(self.dataset_fs.get(dataset_id).read())
            pc = self.db.Dataset.find(kwargs)
            print("[Database] Find one dataset SUCCESS, {} took: {}s".format(kwargs, round(time.time() - s, 2)))

            # check whether more datasets match the requirement
            dataset_id_list = pc.distinct('dataset_id')
            n_dataset = len(dataset_id_list)
            if n_dataset != 1:
                print("     Note that there are {} datasets match the requirement".format(n_dataset))
            return dataset
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.info("{}  {}  {}  {}  {}".format(exc_type, exc_obj, fname, exc_tb.tb_lineno, e))
            return False