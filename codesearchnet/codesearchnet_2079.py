def tf_step(self, x, iteration, conjugate, residual, squared_residual):
        """
        Iteration loop body of the conjugate gradient algorithm.

        Args:
            x: Current solution estimate $x_t$.
            iteration: Current iteration counter $t$.
            conjugate: Current conjugate $c_t$.
            residual: Current residual $r_t$.
            squared_residual: Current squared residual $r_t^2$.

        Returns:
            Updated arguments for next iteration.
        """
        x, next_iteration, conjugate, residual, squared_residual = super(ConjugateGradient, self).tf_step(
            x, iteration, conjugate, residual, squared_residual
        )

        # Ac := A * c_t
        A_conjugate = self.fn_x(conjugate)

        # TODO: reference?
        if self.damping > 0.0:
            A_conjugate = [A_conj + self.damping * conj for A_conj, conj in zip(A_conjugate, conjugate)]

        # cAc := c_t^T * Ac
        conjugate_A_conjugate = tf.add_n(
            inputs=[tf.reduce_sum(input_tensor=(conj * A_conj)) for conj, A_conj in zip(conjugate, A_conjugate)]
        )

        # \alpha := r_t^2 / cAc
        alpha = squared_residual / tf.maximum(x=conjugate_A_conjugate, y=util.epsilon)

        # x_{t+1} := x_t + \alpha * c_t
        next_x = [t + alpha * conj for t, conj in zip(x, conjugate)]

        # r_{t+1} := r_t - \alpha * Ac
        next_residual = [res - alpha * A_conj for res, A_conj in zip(residual, A_conjugate)]

        # r_{t+1}^2 := r_{t+1}^T * r_{t+1}
        next_squared_residual = tf.add_n(inputs=[tf.reduce_sum(input_tensor=(res * res)) for res in next_residual])

        # \beta = r_{t+1}^2 / r_t^2
        beta = next_squared_residual / tf.maximum(x=squared_residual, y=util.epsilon)

        # c_{t+1} := r_{t+1} + \beta * c_t
        next_conjugate = [res + beta * conj for res, conj in zip(next_residual, conjugate)]

        return next_x, next_iteration, next_conjugate, next_residual, next_squared_residual