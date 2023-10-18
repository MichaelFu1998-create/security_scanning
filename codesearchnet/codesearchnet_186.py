def is_propagating(self, images, augmenter, parents, default):
        """
        Returns whether an augmenter may call its children to augment an
        image. This is independent of the augmenter itself possible changing
        the image, without calling its children. (Most (all?) augmenters with
        children currently dont perform any changes themselves.)

        Returns
        -------
        bool
            If True, the augmenter may be propagate to its children. If False, it may not.

        """
        if self.propagator is None:
            return default
        else:
            return self.propagator(images, augmenter, parents, default)