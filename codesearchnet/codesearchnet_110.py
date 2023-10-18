def to_keypoint_image(self, size=1):
        """
        Draws a new black image of shape ``(H,W,N)`` in which all keypoint coordinates are set to 255.
        (H=shape height, W=shape width, N=number of keypoints)

        This function can be used as a helper when augmenting keypoints with a method that only supports the
        augmentation of images.

        Parameters
        -------
        size : int
            Size of each (squared) point.

        Returns
        -------
        image : (H,W,N) ndarray
            Image in which the keypoints are marked. H is the height,
            defined in KeypointsOnImage.shape[0] (analogous W). N is the
            number of keypoints.

        """
        ia.do_assert(len(self.keypoints) > 0)
        height, width = self.shape[0:2]
        image = np.zeros((height, width, len(self.keypoints)), dtype=np.uint8)
        ia.do_assert(size % 2 != 0)
        sizeh = max(0, (size-1)//2)
        for i, keypoint in enumerate(self.keypoints):
            # TODO for float values spread activation over several cells
            # here and do voting at the end
            y = keypoint.y_int
            x = keypoint.x_int

            x1 = np.clip(x - sizeh, 0, width-1)
            x2 = np.clip(x + sizeh + 1, 0, width)
            y1 = np.clip(y - sizeh, 0, height-1)
            y2 = np.clip(y + sizeh + 1, 0, height)

            if x1 < x2 and y1 < y2:
                image[y1:y2, x1:x2, i] = 128
            if 0 <= y < height and 0 <= x < width:
                image[y, x, i] = 255
        return image