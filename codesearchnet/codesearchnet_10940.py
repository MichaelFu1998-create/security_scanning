def save_photon_hdf5(self, identity=None, overwrite=True, path=None):
        """Create a smFRET Photon-HDF5 file with current timestamps."""
        filepath = self.filepath
        if path is not None:
            filepath = Path(path, filepath.name)
        self.merge_da()
        data = self._make_photon_hdf5(identity=identity)
        phc.hdf5.save_photon_hdf5(data, h5_fname=str(filepath),
                                  overwrite=overwrite)