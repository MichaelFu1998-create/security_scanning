def to_xyxy_array(self, dtype=np.float32):
        """
        Convert the BoundingBoxesOnImage object to an (N,4) ndarray.

        This is the inverse of :func:`imgaug.BoundingBoxesOnImage.from_xyxy_array`.

        Parameters
        ----------
        dtype : numpy.dtype, optional
            Desired output datatype of the ndarray.

        Returns
        -------
        ndarray
            (N,4) ndarray array, where ``N`` denotes the number of bounding boxes and ``4`` denotes the
            top-left and bottom-right bounding box corner coordinates in form ``(x1, y1, x2, y2)``.

        """
        xyxy_array = np.zeros((len(self.bounding_boxes), 4), dtype=np.float32)

        for i, box in enumerate(self.bounding_boxes):
            xyxy_array[i] = [box.x1, box.y1, box.x2, box.y2]

        return xyxy_array.astype(dtype)