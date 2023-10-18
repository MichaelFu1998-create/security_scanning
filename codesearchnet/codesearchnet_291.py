def to_keypoints(self):
        """
        Convert the line string points to keypoints.

        Returns
        -------
        list of imgaug.augmentables.kps.Keypoint
            Points of the line string as keypoints.

        """
        # TODO get rid of this deferred import
        from imgaug.augmentables.kps import Keypoint
        return [Keypoint(x=x, y=y) for (x, y) in self.coords]