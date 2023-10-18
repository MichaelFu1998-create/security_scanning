def set_mask(self, mask_img):
        """Sets a mask img to this. So every operation to self, this mask will be taken into account.

        Parameters
        ----------
        mask_img: nifti-like image, NeuroImage or str
            3D mask array: True where a voxel should be used.
            Can either be:
            - a file path to a Nifti image
            - any object with get_data() and get_affine() methods, e.g., nibabel.Nifti1Image.
            If niimg is a string, consider it as a path to Nifti image and
            call nibabel.load on it. If it is an object, check if get_data()
            and get_affine() methods are present, raise TypeError otherwise.

        Note
        ----
        self.img and mask_file must have the same shape.

        Raises
        ------
        FileNotFound, NiftiFilesNotCompatible
        """
        mask = load_mask(mask_img, allow_empty=True)
        check_img_compatibility(self.img, mask, only_check_3d=True) # this will raise an exception if something is wrong
        self.mask = mask