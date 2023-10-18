def apply_mask(self, mask_img):
        """First set_mask and the get_masked_data.

        Parameters
        ----------
        mask_img:  nifti-like image, NeuroImage or str
            3D mask array: True where a voxel should be used.
            Can either be:
            - a file path to a Nifti image
            - any object with get_data() and get_affine() methods, e.g., nibabel.Nifti1Image.
            If niimg is a string, consider it as a path to Nifti image and
            call nibabel.load on it. If it is an object, check if get_data()
            and get_affine() methods are present, raise TypeError otherwise.

        Returns
        -------
        The masked data deepcopied
        """
        self.set_mask(mask_img)
        return self.get_data(masked=True, smoothed=True, safe_copy=True)