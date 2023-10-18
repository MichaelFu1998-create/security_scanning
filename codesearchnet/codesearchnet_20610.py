def create_empty_dataset(self, ds_name, dtype=np.float32):
        """
        Creates a Dataset with unknown size.
        Resize it before using.

        :param ds_name: string

        :param dtype: dtype
        Datatype of the dataset

        :return: h5py DataSet
        """
        if ds_name in self._datasets:
            return self._datasets[ds_name]

        ds = self._group.create_dataset(ds_name, (1, 1), maxshape=None,
                                        dtype=dtype)
        self._datasets[ds_name] = ds

        return ds