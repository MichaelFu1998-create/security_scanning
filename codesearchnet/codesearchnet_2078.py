def tf_initialize(self, x_init, b):
        """
        Initialization step preparing the arguments for the first iteration of the loop body:  
        $x_0, 0, p_0, r_0, r_0^2$.

        Args:
            x_init: Initial solution guess $x_0$, zero vector if None.
            b: The right-hand side $b$ of the system of linear equations.

        Returns:
            Initial arguments for tf_step.
        """
        if x_init is None:
            # Initial guess is zero vector if not given.
            x_init = [tf.zeros(shape=util.shape(t)) for t in b]

        initial_args = super(ConjugateGradient, self).tf_initialize(x_init)

        # r_0 := b - A * x_0
        # c_0 := r_0
        conjugate = residual = [t - fx for t, fx in zip(b, self.fn_x(x_init))]

        # r_0^2 := r^T * r
        squared_residual = tf.add_n(inputs=[tf.reduce_sum(input_tensor=(res * res)) for res in residual])

        return initial_args + (conjugate, residual, squared_residual)