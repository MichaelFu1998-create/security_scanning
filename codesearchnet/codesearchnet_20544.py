def to_matrix(self, smooth_fwhm=0, outdtype=None):
        """Return numpy.ndarray with the masked or flatten image data and
           the relevant information (mask indices and volume shape).

        Parameters
        ----------
        smooth__fwhm: int
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
        if not self.all_compatible:
            raise ValueError("`self.all_compatible` must be True in order to use this function.")

        if not outdtype:
            outdtype = self.items[0].dtype

        # extract some info from the mask
        n_voxels     = None
        mask_indices = None
        mask_shape   = self.items[0].shape[:3]
        if self.has_mask:
            mask_arr     = self.mask.get_data()
            mask_indices = np.nonzero(mask_arr)
            mask_shape   = self.mask.shape
            n_voxels     = np.count_nonzero(mask_arr)

        # if the mask is empty will use the whole image
        if n_voxels is None:
            log.debug('Non-zero voxels have not been found in mask {}'.format(self.mask))
            n_voxels     = np.prod(mask_shape)
            mask_indices = None

        # get the shape of the flattened subject data
        ndims = self.items[0].ndim
        if ndims == 3:
            subj_flat_shape = (n_voxels, )
        elif ndims == 4:
            subj_flat_shape = (n_voxels, self.items[0].shape[3])
        else:
            raise NotImplementedError('The subject images have {} dimensions. '
                                      'Still have not implemented t_matrix for this shape.'.format(ndims))

        # create and fill the big matrix
        outmat = np.zeros((self.n_subjs, ) + subj_flat_shape, dtype=outdtype)
        try:
            for i, image in enumerate(self.items):
                if smooth_fwhm > 0:
                    image.fwhm = smooth_fwhm

                if self.has_mask:
                    image.set_mask(self.mask)

                outmat[i, :], _, _ = image.mask_and_flatten()
                image.clear_data()

        except Exception as exc:
            raise Exception('Error flattening file {0}'.format(image)) from exc
        else:
            return outmat, mask_indices, mask_shape