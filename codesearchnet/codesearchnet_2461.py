def predictions(self, image):
        """Convenience method that calculates predictions for a single image.

        Parameters
        ----------
        image : `numpy.ndarray`
            Single input with shape as expected by the model
            (without the batch dimension).

        Returns
        -------
        `numpy.ndarray`
            Vector of predictions (logits, i.e. before the softmax) with
            shape (number of classes,).

        See Also
        --------
        :meth:`batch_predictions`

        """
        return np.squeeze(self.batch_predictions(image[np.newaxis]), axis=0)