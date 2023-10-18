def mask(self, image):
        """ self.mask setter

        Parameters
        ----------
        image: str or img-like object.
            See NeuroImage constructor docstring.
        """
        if image is None:
            self._mask = None

        try:
            mask = load_mask(image)
        except Exception as exc:
            raise Exception('Could not load mask image {}.'.format(image)) from exc
        else:
            self._mask = mask