def create_for_noise(other_param, threshold=(-10, 10), activated=True):
        """
        Creates a Sigmoid that is adjusted to be used with noise parameters,
        i.e. with parameters which's output values are in the range [0.0, 1.0].

        Parameters
        ----------
        other_param : imgaug.parameters.StochasticParameter
            See :func:`imgaug.parameters.Sigmoid.__init__`.

        threshold : number or tuple of number or iterable of number or imgaug.parameters.StochasticParameter,\
                    optional
            See :func:`imgaug.parameters.Sigmoid.__init__`.

        activated : bool or number, optional
            See :func:`imgaug.parameters.Sigmoid.__init__`.

        Returns
        -------
        Sigmoid
            A sigmoid adjusted to be used with noise.

        """
        return Sigmoid(other_param, threshold, activated, mul=20, add=-10)