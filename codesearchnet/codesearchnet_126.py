def shift(self, top=None, right=None, bottom=None, left=None):
        """
        Shift the bounding box from one or more image sides, i.e. move it on the x/y-axis.

        Parameters
        ----------
        top : None or int, optional
            Amount of pixels by which to shift the bounding box from the top.

        right : None or int, optional
            Amount of pixels by which to shift the bounding box from the right.

        bottom : None or int, optional
            Amount of pixels by which to shift the bounding box from the bottom.

        left : None or int, optional
            Amount of pixels by which to shift the bounding box from the left.

        Returns
        -------
        result : imgaug.BoundingBox
            Shifted bounding box.

        """
        top = top if top is not None else 0
        right = right if right is not None else 0
        bottom = bottom if bottom is not None else 0
        left = left if left is not None else 0
        return self.copy(
            x1=self.x1+left-right,
            x2=self.x2+left-right,
            y1=self.y1+top-bottom,
            y2=self.y2+top-bottom
        )