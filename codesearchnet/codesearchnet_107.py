def shift(self, x=0, y=0):
        """
        Move the keypoints around on an image.

        Parameters
        ----------
        x : number, optional
            Move each keypoint by this value on the x axis.

        y : number, optional
            Move each keypoint by this value on the y axis.

        Returns
        -------
        out : KeypointsOnImage
            Keypoints after moving them.

        """
        keypoints = [keypoint.shift(x=x, y=y) for keypoint in self.keypoints]
        return self.deepcopy(keypoints)