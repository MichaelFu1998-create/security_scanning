def on(self, image):
        """
        Project bounding boxes from one image to a new one.

        Parameters
        ----------
        image : ndarray or tuple of int
            The new image onto which to project.
            Either an image with shape ``(H,W,[C])`` or a tuple denoting
            such an image shape.

        Returns
        -------
        line_strings : imgaug.augmentables.lines.LineStrings
            Object containing all projected line strings.

        """
        shape = normalize_shape(image)
        if shape[0:2] == self.shape[0:2]:
            return self.deepcopy()
        line_strings = [ls.project(self.shape, shape)
                        for ls in self.line_strings]
        return self.deepcopy(line_strings=line_strings, shape=shape)