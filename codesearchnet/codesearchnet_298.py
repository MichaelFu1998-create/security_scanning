def copy(self, coords=None, label=None):
        """
        Create a shallow copy of the LineString object.

        Parameters
        ----------
        coords : None or iterable of tuple of number or ndarray
            If not ``None``, then the coords of the copied object will be set
            to this value.

        label : None or str
            If not ``None``, then the label of the copied object will be set to
            this value.

        Returns
        -------
        imgaug.augmentables.lines.LineString
            Shallow copy.

        """
        return LineString(coords=self.coords if coords is None else coords,
                          label=self.label if label is None else label)