def pad_to_aspect_ratio(self, aspect_ratio, mode="constant", cval=0.0, return_pad_amounts=False):
        """
        Pad the segmentation map on its sides so that its matches a target aspect ratio.

        Depending on which dimension is smaller (height or width), only the corresponding
        sides (left/right or top/bottom) will be padded. In each case, both of the sides will
        be padded equally.

        Parameters
        ----------
        aspect_ratio : float
            Target aspect ratio, given as width/height. E.g. 2.0 denotes the image having twice
            as much width as height.

        mode : str, optional
            Padding mode to use. See :func:`numpy.pad` for details.

        cval : number, optional
            Value to use for padding if `mode` is ``constant``. See :func:`numpy.pad` for details.

        return_pad_amounts : bool, optional
            If False, then only the padded image will be returned. If True, a tuple with two
            entries will be returned, where the first entry is the padded image and the second
            entry are the amounts by which each image side was padded. These amounts are again a
            tuple of the form (top, right, bottom, left), with each value being an integer.

        Returns
        -------
        segmap : imgaug.SegmentationMapOnImage
            Padded segmentation map as SegmentationMapOnImage object.

        pad_amounts : tuple of int
            Amounts by which the segmentation map was padded on each side, given as a
            tuple ``(top, right, bottom, left)``.
            This tuple is only returned if `return_pad_amounts` was set to True.

        """
        arr_padded, pad_amounts = ia.pad_to_aspect_ratio(self.arr, aspect_ratio=aspect_ratio, mode=mode, cval=cval,
                                                         return_pad_amounts=True)
        segmap = SegmentationMapOnImage(arr_padded, shape=self.shape)
        segmap.input_was = self.input_was
        if return_pad_amounts:
            return segmap, pad_amounts
        else:
            return segmap