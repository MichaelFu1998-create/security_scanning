def copy(self, keypoints=None, shape=None):
        """
        Create a shallow copy of the KeypointsOnImage object.

        Parameters
        ----------
        keypoints : None or list of imgaug.Keypoint, optional
            List of keypoints on the image. If ``None``, the instance's
            keypoints will be copied.

        shape : tuple of int, optional
            The shape of the image on which the keypoints are placed.
            If ``None``, the instance's shape will be copied.

        Returns
        -------
        imgaug.KeypointsOnImage
            Shallow copy.

        """
        result = copy.copy(self)
        if keypoints is not None:
            result.keypoints = keypoints
        if shape is not None:
            result.shape = shape
        return result