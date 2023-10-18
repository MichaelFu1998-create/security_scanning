def from_xy_array(cls, xy, shape):
        """
        Convert an array (N,2) with a given image shape to a KeypointsOnImage object.

        Parameters
        ----------
        xy : (N, 2) ndarray
            Coordinates of ``N`` keypoints on the original image, given
            as ``(N,2)`` array of xy-coordinates.

        shape : tuple of int or ndarray
            Shape tuple of the image on which the keypoints are placed.

        Returns
        -------
        KeypointsOnImage
            KeypointsOnImage object that contains all keypoints from the array.

        """
        keypoints = [Keypoint(x=coord[0], y=coord[1]) for coord in xy]
        return KeypointsOnImage(keypoints, shape)