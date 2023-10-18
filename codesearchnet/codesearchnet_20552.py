def to_matrix(self, smooth_fwhm=0, outdtype=None):
        """Create a Numpy array with the data and return the relevant information (mask indices and volume shape).

        Parameters
        ----------
        smooth_fwhm: int
            Integer indicating the size of the FWHM Gaussian smoothing kernel
            to smooth the subject volumes before creating the data matrix

        outdtype: dtype
            Type of the elements of the array, if None will obtain the dtype from
            the first nifti file.

        Returns
        -------
        outmat, mask_indices, vol_shape

        outmat: Numpy array with shape N x prod(vol.shape)
                containing the N files as flat vectors.

        mask_indices: matrix with indices of the voxels in the mask

        vol_shape: Tuple with shape of the volumes, for reshaping.
        """

        vol = self.items[0].get_data()
        if not outdtype:
            outdtype = vol.dtype

        n_voxels     = None
        mask_indices = None
        mask_shape   = self.items[0].shape

        if self.has_mask:
            mask_arr     = get_img_data(self.mask_file)
            mask_indices = np.where(mask_arr > 0)
            mask_shape   = mask_arr.shape
            n_voxels     = np.count_nonzero(mask_arr)

        if n_voxels is None:
            log.debug('Non-zero voxels have not been found in mask {}'.format(self.mask_file))
            n_voxels = np.prod(vol.shape)

        outmat = np.zeros((self.n_subjs, n_voxels), dtype=outdtype)
        try:
            for i, nipy_img in enumerate(self.items):
                vol = self._smooth_img(nipy_img, smooth_fwhm).get_data()
                if self.has_mask is not None:
                    outmat[i, :] = vol[mask_indices]
                else:
                    outmat[i, :] = vol.flatten()
        except Exception as exc:
            raise Exception('Error when flattening file {0}'.format(nipy_img.file_path)) from exc
        else:
            return outmat, mask_indices, mask_shape