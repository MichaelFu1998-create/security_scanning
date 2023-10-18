def deepcopy(self, coords=None, label=None):
        """
        Create a deep copy of the BoundingBox object.

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
            Deep copy.

        """
        return LineString(
            coords=np.copy(self.coords) if coords is None else coords,
            label=copylib.deepcopy(self.label) if label is None else label)