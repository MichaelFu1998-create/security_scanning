def copy(self, x1=None, y1=None, x2=None, y2=None, label=None):
        """
        Create a shallow copy of the BoundingBox object.

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
            Shallow copy.

        """
        return BoundingBox(
            x1=self.x1 if x1 is None else x1,
            x2=self.x2 if x2 is None else x2,
            y1=self.y1 if y1 is None else y1,
            y2=self.y2 if y2 is None else y2,
            label=self.label if label is None else label
        )