def _process_gradient(self, backward, dmdp):
        """
        backward: `callable`
            callable that backpropagates the gradient of the model w.r.t to
            preprocessed input through the preprocessing to get the gradient
            of the model's output w.r.t. the input before preprocessing
        dmdp: gradient of model w.r.t. preprocessed input
        """
        if backward is None:  # pragma: no cover
            raise ValueError('Your preprocessing function does not provide'
                             ' an (approximate) gradient')
        dmdx = backward(dmdp)
        assert dmdx.dtype == dmdp.dtype
        return dmdx