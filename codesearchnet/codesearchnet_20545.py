def to_file(self, output_file, smooth_fwhm=0, outdtype=None):
        """Save the Numpy array created from to_matrix function to the output_file.

        Will save into the file: outmat, mask_indices, vol_shape and self.others (put here whatever you want)

            data: Numpy array with shape N x prod(vol.shape)
                  containing the N files as flat vectors.

            mask_indices: matrix with indices of the voxels in the mask

            vol_shape: Tuple with shape of the volumes, for reshaping.

        Parameters
        ----------
        output_file: str
            Path to the output file. The extension of the file will be taken into account for the file format.
            Choices of extensions: '.pyshelf' or '.shelf' (Python shelve)
                                   '.mat' (Matlab archive),
                                   '.hdf5' or '.h5' (HDF5 file)

        smooth_fwhm: int
            Integer indicating the size of the FWHM Gaussian smoothing kernel
            to smooth the subject volumes before creating the data matrix

        outdtype: dtype
            Type of the elements of the array, if None will obtain the dtype from
            the first nifti file.
        """
        outmat, mask_indices, mask_shape = self.to_matrix(smooth_fwhm, outdtype)

        exporter = ExportData()
        content = {'data':         outmat,
                   'labels':       self.labels,
                   'mask_indices': mask_indices,
                   'mask_shape':   mask_shape, }

        if self.others:
            content.update(self.others)

        log.debug('Creating content in file {}.'.format(output_file))
        try:
            exporter.save_variables(output_file, content)
        except Exception as exc:
            raise Exception('Error saving variables to file {}.'.format(output_file)) from exc