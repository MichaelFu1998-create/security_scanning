def deepcopy(self, exterior=None, label=None):
        """
        Create a deep copy of the Polygon object.

        Parameters
        ----------
        exterior : list of Keypoint or list of tuple or (N,2) ndarray, optional
            List of points defining the polygon. See `imgaug.Polygon.__init__` for details.

        label : None or str
            If not None, then the label of the copied object will be set to this value.

        Returns
        -------
        imgaug.Polygon
            Deep copy.

        """
        return Polygon(
            exterior=np.copy(self.exterior) if exterior is None else exterior,
            label=self.label if label is None else label
        )