def copy(self, x=None, y=None):
        """
        Create a shallow copy of the Keypoint object.

        Parameters
        ----------
        x : None or number, optional
            Coordinate of the keypoint on the x axis.
            If ``None``, the instance's value will be copied.

        y : None or number, optional
            Coordinate of the keypoint on the y axis.
            If ``None``, the instance's value will be copied.

        Returns
        -------
        imgaug.Keypoint
            Shallow copy.

        """
        return self.deepcopy(x=x, y=y)