def _load_image(file_path):
        """
        Parameters
        ----------
        file_path: str
            Path to the nifti file

        Returns
        -------
        nipy.Image with a file_path member
        """
        if not os.path.exists(file_path):
            raise FileNotFound(file_path)

        try:
            nii_img           = load_nipy_img(file_path)
            nii_img.file_path = file_path
            return nii_img
        except Exception as exc:
            raise Exception('Reading file {0}.'.format(file_path)) from exc