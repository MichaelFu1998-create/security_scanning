def to_keypoints(self):
        """
        Convert the corners of the bounding box to keypoints (clockwise, starting at top left).

        Returns
        -------
        list of imgaug.Keypoint
            Corners of the bounding box as keypoints.

        """
        # TODO get rid of this deferred import
        from imgaug.augmentables.kps import Keypoint

        return [
            Keypoint(x=self.x1, y=self.y1),
            Keypoint(x=self.x2, y=self.y1),
            Keypoint(x=self.x2, y=self.y2),
            Keypoint(x=self.x1, y=self.y2)
        ]