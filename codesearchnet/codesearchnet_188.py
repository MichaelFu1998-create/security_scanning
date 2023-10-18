def postprocess(self, images, augmenter, parents):
        """
        A function to be called after the augmentation of images was
        performed.

        Returns
        -------
        (N,H,W,C) ndarray or (N,H,W) ndarray or list of (H,W,C) ndarray or list of (H,W) ndarray
            The input images, optionally modified.

        """
        if self.postprocessor is None:
            return images
        else:
            return self.postprocessor(images, augmenter, parents)