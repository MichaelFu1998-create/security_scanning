def copy(self, line_strings=None, shape=None):
        """
        Create a shallow copy of the LineStringsOnImage object.

        Parameters
        ----------
        line_strings : None \
                       or list of imgaug.augmentables.lines.LineString, optional
            List of line strings on the image.
            If not ``None``, then the ``line_strings`` attribute of the copied
            object will be set to this value.

        shape : None or tuple of int or ndarray, optional
            The shape of the image on which the objects are placed.
            Either an image with shape ``(H,W,[C])`` or a tuple denoting
            such an image shape.
            If not ``None``, then the ``shape`` attribute of the copied object
            will be set to this value.

        Returns
        -------
        imgaug.augmentables.lines.LineStringsOnImage
            Shallow copy.

        """
        lss = self.line_strings if line_strings is None else line_strings
        shape = self.shape if shape is None else shape
        return LineStringsOnImage(line_strings=lss, shape=shape)