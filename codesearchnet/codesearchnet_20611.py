def create_dataset(self, ds_name, data, attrs=None, dtype=None):
        """
        Saves a Numpy array in a dataset in the HDF file, registers it as
        ds_name and returns the h5py dataset.

        :param ds_name: string
        Registration name of the dataset to be registered.

        :param data: Numpy ndarray

        :param dtype: dtype
        Datatype of the dataset

        :return: h5py dataset
        """
        if ds_name in self._datasets:
            ds = self._datasets[ds_name]
            if ds.dtype != data.dtype:
                warnings.warn('Dataset and data dtype are different!')

        else:
            if dtype is None:
                dtype = data.dtype

            ds = self._group.create_dataset(ds_name, data.shape,
                                            dtype=dtype)

            if attrs is not None:
                for key in attrs:
                    setattr(ds.attrs, key, attrs[key])

        ds.read_direct(data)
        self._datasets[ds_name] = ds

        return ds