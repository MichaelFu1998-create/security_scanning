def to_hdf5(self, file_handle, parent_node='/'):
        """Store the PSF data in `file_handle` (pytables) in `parent_node`.

        The raw PSF array name is stored with same name as the original fname.
        Also, the following attribues are set: fname, dir_, x_step, z_step.
        """
        tarray = file_handle.create_array(parent_node, name=self.fname,
                                          obj=self.psflab_psf_raw,
                                          title='PSF x-z slice (PSFLab array)')
        for name in ['fname', 'dir_', 'x_step', 'z_step']:
            file_handle.set_node_attr(tarray, name, getattr(self, name))
        return tarray