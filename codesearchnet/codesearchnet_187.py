def preprocess(self, images, augmenter, parents):
        """
        A function to be called before the augmentation of images starts (per augmenter).

        Returns
        -------
        (N,H,W,C) ndarray or (N,H,W) ndarray or list of (H,W,C) ndarray or list of (H,W) ndarray
            The input images, optionally modified.

        """
        if self.preprocessor is None:
            return images
        else:
            return self.preprocessor(images, augmenter, parents)