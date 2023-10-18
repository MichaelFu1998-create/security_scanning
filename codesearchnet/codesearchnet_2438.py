def __is_adversarial(self, image, predictions, in_bounds):
        """Interface to criterion.is_adverarial that calls
        __new_adversarial if necessary.

        Parameters
        ----------
        predictions : :class:`numpy.ndarray`
            A vector with the pre-softmax predictions for some image.
        label : int
            The label of the unperturbed reference image.

        """
        is_adversarial = self.__criterion.is_adversarial(
            predictions, self.__original_class)
        assert isinstance(is_adversarial, bool) or \
            isinstance(is_adversarial, np.bool_)
        if is_adversarial:
            is_best, distance = self.__new_adversarial(
                image, predictions, in_bounds)
        else:
            is_best = False
            distance = None
        return is_adversarial, is_best, distance