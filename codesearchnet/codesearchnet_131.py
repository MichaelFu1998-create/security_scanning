def deepcopy(self, x1=None, y1=None, x2=None, y2=None, label=None):
        """
        Create a deep copy of the BoundingBox object.

        Parameters
        ----------
        x1 : None or number
            If not None, then the x1 coordinate of the copied object will be set to this value.

        y1 : None or number
            If not None, then the y1 coordinate of the copied object will be set to this value.

        x2 : None or number
            If not None, then the x2 coordinate of the copied object will be set to this value.

        y2 : None or number
            If not None, then the y2 coordinate of the copied object will be set to this value.

        label : None or string
            If not None, then the label of the copied object will be set to this value.

        Returns
        -------
        imgaug.BoundingBox
            Deep copy.

        """
        return self.copy(x1=x1, y1=y1, x2=x2, y2=y2, label=label)