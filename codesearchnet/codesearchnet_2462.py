def gradient(self, image, label):
        """Calculates the gradient of the cross-entropy loss w.r.t. the image.

        The default implementation calls predictions_and_gradient.
        Subclasses can provide more efficient implementations that
        only calculate the gradient.

        Parameters
        ----------
        image : `numpy.ndarray`
            Single input with shape as expected by the model
            (without the batch dimension).
        label : int
            Reference label used to calculate the gradient.

        Returns
        -------
        gradient : `numpy.ndarray`
            The gradient of the cross-entropy loss w.r.t. the image. Will
            have the same shape as the image.

        See Also
        --------
        :meth:`gradient`

        """
        _, gradient = self.predictions_and_gradient(image, label)
        return gradient