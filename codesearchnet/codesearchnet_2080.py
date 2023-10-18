def tf_next_step(self, x, iteration, conjugate, residual, squared_residual):
        """
        Termination condition: max number of iterations, or residual sufficiently small.

        Args:
            x: Current solution estimate $x_t$.
            iteration: Current iteration counter $t$.
            conjugate: Current conjugate $c_t$.
            residual: Current residual $r_t$.
            squared_residual: Current squared residual $r_t^2$.

        Returns:
            True if another iteration should be performed.
        """
        next_step = super(ConjugateGradient, self).tf_next_step(x, iteration, conjugate, residual, squared_residual)
        return tf.logical_and(x=next_step, y=(squared_residual >= util.epsilon))