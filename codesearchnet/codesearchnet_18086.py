def set_image(self, image):
        """
        Update the current comparison (real) image
        """
        if isinstance(image, np.ndarray):
            image = util.Image(image)

        if isinstance(image, util.NullImage):
            self.model_as_data = True
        else:
            self.model_as_data = False

        self.image = image
        self._data = self.image.get_padded_image(self.pad)

        # set up various slicers and Tiles associated with the image and pad
        self.oshape = util.Tile(self._data.shape)
        self.ishape = self.oshape.pad(-self.pad)
        self.inner = self.ishape.slicer

        for c in self.comps:
            c.set_shape(self.oshape, self.ishape)

        self._model = np.zeros(self._data.shape, dtype=np.float64)
        self._residuals = np.zeros(self._data.shape, dtype=np.float64)
        self.calculate_model()