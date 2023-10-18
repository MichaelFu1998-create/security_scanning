def predictions_and_gradient(
            self, image=None, label=None, strict=True, return_details=False):
        """Interface to model.predictions_and_gradient for attacks.

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

        in_bounds = self.in_bounds(image)
        assert not strict or in_bounds

        self._total_prediction_calls += 1
        self._total_gradient_calls += 1
        predictions, gradient = self.__model.predictions_and_gradient(image, label)  # noqa: E501
        is_adversarial, is_best, distance = self.__is_adversarial(
            image, predictions, in_bounds)

        assert predictions.ndim == 1
        assert gradient.shape == image.shape
        if return_details:
            return predictions, gradient, is_adversarial, is_best, distance
        else:
            return predictions, gradient, is_adversarial