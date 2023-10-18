def deepcopy(self, x=None, y=None):
        """
        Create a deep copy of the Keypoint object.

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
            Deep copy.

        """
        x = self.x if x is None else x
        y = self.y if y is None else y
        return Keypoint(x=x, y=y)