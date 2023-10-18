def from_xyxy_array(cls, xyxy, shape):
        """
        Convert an (N,4) ndarray to a BoundingBoxesOnImage object.

        This is the inverse of :func:`imgaug.BoundingBoxesOnImage.to_xyxy_array`.

        Parameters
        ----------
        xyxy : (N,4) ndarray
            Array containing the corner coordinates (top-left, bottom-right) of ``N`` bounding boxes
            in the form ``(x1, y1, x2, y2)``. Should usually be of dtype ``float32``.

        shape : tuple of int
            Shape of the image on which the bounding boxes are placed.
            Should usually be ``(H, W, C)`` or ``(H, W)``.

        Returns
        -------
        imgaug.BoundingBoxesOnImage
            Object containing a list of BoundingBox objects following the provided corner coordinates.

        """
        ia.do_assert(xyxy.shape[1] == 4, "Expected input array of shape (N, 4), got shape %s." % (xyxy.shape,))

        boxes = [BoundingBox(*row) for row in xyxy]

        return cls(boxes, shape)