def gradient(self, image=None, label=None, strict=True):
        """Interface to model.gradient for attacks.

        Parameters
        ----------
        image : `numpy.ndarray`
            Single input with shape as expected by the model
            (without the batch dimension).
            Defaults to the original image.
        label : int
            Label used to calculate the loss that is differentiated.
            Defaults to the original label.
        strict : bool
            Controls if the bounds for the pixel values should be checked.

        """
        assert self.has_gradient()

        if image is None:
            image = self.__original_image
        if label is None:
            label = self.__original_class

        assert not strict or self.in_bounds(image)

        self._total_gradient_calls += 1
        gradient = self.__model.gradient(image, label)

        assert gradient.shape == image.shape
        return gradient