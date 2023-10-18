def backward(self, gradient, image=None, strict=True):
        """Interface to model.backward for attacks.

        Parameters
        ----------
        gradient : `numpy.ndarray`
            Gradient of some loss w.r.t. the logits.
        image : `numpy.ndarray`
            Single input with shape as expected by the model
            (without the batch dimension).

        Returns
        -------
        gradient : `numpy.ndarray`
            The gradient w.r.t the image.

        See Also
        --------
        :meth:`gradient`

        """
        assert self.has_gradient()
        assert gradient.ndim == 1

        if image is None:
            image = self.__original_image

        assert not strict or self.in_bounds(image)

        self._total_gradient_calls += 1
        gradient = self.__model.backward(gradient, image)

        assert gradient.shape == image.shape
        return gradient