def create_hdf_file(self):
        """
        :return: h5py DataSet
        """
        mode = 'w'
        if not self._overwrite and os.path.exists(self._fname):
            mode = 'a'

        self._hdf_file = h5py.File(self._fname, mode)

        if self._hdf_basepath == '/':
            self._group = self._hdf_file['/']
        else:
            self._group = self._hdf_file.create_group(self._hdf_basepath)