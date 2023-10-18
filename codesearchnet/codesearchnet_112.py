def to_distance_maps(self, inverted=False):
        """
        Generates a ``(H,W,K)`` output containing ``K`` distance maps for ``K`` keypoints.

        The k-th distance map contains at every location ``(y, x)`` the euclidean distance to the k-th keypoint.

        This function can be used as a helper when augmenting keypoints with a method that only supports
        the augmentation of images.

        Parameters
        -------
        inverted : bool, optional
            If True, inverted distance maps are returned where each distance value d is replaced
            by ``d/(d+1)``, i.e. the distance maps have values in the range ``(0.0, 1.0]`` with 1.0
            denoting exactly the position of the respective keypoint.

        Returns
        -------
        distance_maps : (H,W,K) ndarray
            A ``float32`` array containing ``K`` distance maps for ``K`` keypoints. Each location
            ``(y, x, k)`` in the array denotes the euclidean distance at ``(y, x)`` to the ``k``-th keypoint.
            In inverted mode the distance ``d`` is replaced by ``d/(d+1)``. The height and width
            of the array match the height and width in ``KeypointsOnImage.shape``.

        """
        ia.do_assert(len(self.keypoints) > 0)
        height, width = self.shape[0:2]
        distance_maps = np.zeros((height, width, len(self.keypoints)), dtype=np.float32)

        yy = np.arange(0, height)
        xx = np.arange(0, width)
        grid_xx, grid_yy = np.meshgrid(xx, yy)

        for i, keypoint in enumerate(self.keypoints):
            y, x = keypoint.y, keypoint.x
            distance_maps[:, :, i] = (grid_xx - x) ** 2 + (grid_yy - y) ** 2
        distance_maps = np.sqrt(distance_maps)
        if inverted:
            return 1/(distance_maps+1)
        return distance_maps