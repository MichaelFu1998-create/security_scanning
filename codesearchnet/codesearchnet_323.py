def pad(self, top=0, right=0, bottom=0, left=0, mode="constant", cval=0.0):
        """
        Pad the segmentation map on its top/right/bottom/left side.

        Parameters
        ----------
        top : int, optional
            Amount of pixels to add at the top side of the segmentation map. Must be 0 or greater.

        right : int, optional
            Amount of pixels to add at the right side of the segmentation map. Must be 0 or greater.

        bottom : int, optional
            Amount of pixels to add at the bottom side of the segmentation map. Must be 0 or greater.

        left : int, optional
            Amount of pixels to add at the left side of the segmentation map. Must be 0 or greater.

        mode : str, optional
            Padding mode to use. See :func:`numpy.pad` for details.

        cval : number, optional
            Value to use for padding if `mode` is ``constant``. See :func:`numpy.pad` for details.

        Returns
        -------
        segmap : imgaug.SegmentationMapOnImage
            Padded segmentation map of height ``H'=H+top+bottom`` and width ``W'=W+left+right``.

        """
        arr_padded = ia.pad(self.arr, top=top, right=right, bottom=bottom, left=left, mode=mode, cval=cval)
        segmap = SegmentationMapOnImage(arr_padded, shape=self.shape)
        segmap.input_was = self.input_was
        return segmap