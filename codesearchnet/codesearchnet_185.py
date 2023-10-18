def is_activated(self, images, augmenter, parents, default):
        """
        Returns whether an augmenter may be executed.

        Returns
        -------
        bool
            If True, the augmenter may be executed. If False, it may not be executed.

        """
        if self.activator is None:
            return default
        else:
            return self.activator(images, augmenter, parents, default)