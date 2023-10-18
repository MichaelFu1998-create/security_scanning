def get_dataset(self, ds_name, mode='r'):
        """
        Returns a h5py dataset given its registered name.

        :param ds_name: string
        Name of the dataset to be returned.

        :return:
        """
        if ds_name in self._datasets:
            return self._datasets[ds_name]
        else:
            return self.create_empty_dataset(ds_name)