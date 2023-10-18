def to_keypoints(self):
        """
        Convert this polygon's `exterior` to ``Keypoint`` instances.

        Returns
        -------
        list of imgaug.Keypoint
            Exterior vertices as ``Keypoint`` instances.

        """
        # TODO get rid of this deferred import
        from imgaug.augmentables.kps import Keypoint

        return [Keypoint(x=point[0], y=point[1]) for point in self.exterior]