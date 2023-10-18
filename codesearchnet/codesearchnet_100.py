def shift(self, x=0, y=0):
        """
        Move the keypoint around on an image.

        Parameters
        ----------
        x : number, optional
            Move by this value on the x axis.

        y : number, optional
            Move by this value on the y axis.

        Returns
        -------
        imgaug.Keypoint
            Keypoint object with new coordinates.

        """
        return self.deepcopy(self.x + x, self.y + y)