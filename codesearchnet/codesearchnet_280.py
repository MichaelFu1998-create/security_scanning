def shift(self, top=None, right=None, bottom=None, left=None):
        """
        Shift/move the line string from one or more image sides.

        Parameters
        ----------
        top : None or int, optional
            Amount of pixels by which to shift the bounding box from the
            top.

        right : None or int, optional
            Amount of pixels by which to shift the bounding box from the
            right.

        bottom : None or int, optional
            Amount of pixels by which to shift the bounding box from the
            bottom.

        left : None or int, optional
            Amount of pixels by which to shift the bounding box from the
            left.

        Returns
        -------
        result : imgaug.augmentables.lines.LineString
            Shifted line string.

        """
        top = top if top is not None else 0
        right = right if right is not None else 0
        bottom = bottom if bottom is not None else 0
        left = left if left is not None else 0
        coords = np.copy(self.coords)
        coords[:, 0] += left - right
        coords[:, 1] += top - bottom
        return self.copy(coords=coords)