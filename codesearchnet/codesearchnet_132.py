def on(self, image):
        """
        Project bounding boxes from one image to a new one.

        Parameters
        ----------
        image : ndarray or tuple of int
            New image onto which the bounding boxes are to be projected.
            May also simply be that new image's shape tuple.

        Returns
        -------
        bounding_boxes : imgaug.BoundingBoxesOnImage
            Object containing all projected bounding boxes.

        """
        shape = normalize_shape(image)
        if shape[0:2] == self.shape[0:2]:
            return self.deepcopy()
        bounding_boxes = [bb.project(self.shape, shape)
                          for bb in self.bounding_boxes]
        return BoundingBoxesOnImage(bounding_boxes, shape)