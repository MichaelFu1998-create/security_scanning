def copy(self, exterior=None, label=None):
        """
        Create a shallow copy of the Polygon object.

        Parameters
        ----------
        exterior : list of imgaug.Keypoint or list of tuple or (N,2) ndarray, optional
            List of points defining the polygon. See :func:`imgaug.Polygon.__init__` for details.

        label : None or str, optional
            If not None, then the label of the copied object will be set to this value.

        Returns
        -------
        imgaug.Polygon
            Shallow copy.

        """
        return self.deepcopy(exterior=exterior, label=label)