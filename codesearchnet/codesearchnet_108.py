def to_xy_array(self):
        """
        Convert keypoint coordinates to ``(N,2)`` array.

        Returns
        -------
        (N, 2) ndarray
            Array containing the coordinates of all keypoints.
            Shape is ``(N,2)`` with coordinates in xy-form.

        """
        result = np.zeros((len(self.keypoints), 2), dtype=np.float32)
        for i, keypoint in enumerate(self.keypoints):
            result[i, 0] = keypoint.x
            result[i, 1] = keypoint.y
        return result