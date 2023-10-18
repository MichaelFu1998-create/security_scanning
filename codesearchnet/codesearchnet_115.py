def deepcopy(self, keypoints=None, shape=None):
        """
        Create a deep copy of the KeypointsOnImage object.

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
            Deep copy.

        """
        # for some reason deepcopy is way slower here than manual copy
        if keypoints is None:
            keypoints = [kp.deepcopy() for kp in self.keypoints]
        if shape is None:
            shape = tuple(self.shape)
        return KeypointsOnImage(keypoints, shape)