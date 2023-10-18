def find_datasets(self, dataset_name=None, **kwargs):
        """Finds and returns all datasets from the database which matches the requirement.
        In some case, the data in a dataset can be stored separately for better management.

        Parameters
        ----------
        dataset_name : str
            The name/key of dataset.
        kwargs : other events
            Other events, such as description, author and etc (optional).

        Returns
        --------
        params : the parameters, return False if nothing found.

        """

        self._fill_project_info(kwargs)
        if dataset_name is None:
            raise Exception("dataset_name is None, please give a dataset name")
        kwargs.update({'dataset_name': dataset_name})

        s = time.time()
        pc = self.db.Dataset.find(kwargs)

        if pc is not None:
            dataset_id_list = pc.distinct('dataset_id')
            dataset_list = []
            for dataset_id in dataset_id_list:  # you may have multiple Buckets files
                tmp = self.dataset_fs.get(dataset_id).read()
                dataset_list.append(self._deserialization(tmp))
        else:
            print("[Database] FAIL! Cannot find any dataset: {}".format(kwargs))
            return False

        print("[Database] Find {} datasets SUCCESS, took: {}s".format(len(dataset_list), round(time.time() - s, 2)))
        return dataset_list