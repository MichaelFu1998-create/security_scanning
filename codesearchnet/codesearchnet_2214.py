def tf_step(self, x, iteration, deltas, improvement, last_improvement, estimated_improvement):
        """
        Iteration loop body of the line search algorithm.

        Args:
            x: Current solution estimate $x_t$.
            iteration: Current iteration counter $t$.
            deltas: Current difference $x_t - x'$.
            improvement: Current improvement $(f(x_t) - f(x')) / v'$.
            last_improvement: Last improvement $(f(x_{t-1}) - f(x')) / v'$.
            estimated_improvement: Current estimated value $v'$.

        Returns:
            Updated arguments for next iteration.
        """
        x, next_iteration, deltas, improvement, last_improvement, estimated_improvement = super(LineSearch, self).tf_step(
            x, iteration, deltas, improvement, last_improvement, estimated_improvement
        )

        next_x = [t + delta for t, delta in zip(x, deltas)]

        if self.mode == 'linear':
            next_deltas = deltas
            next_estimated_improvement = estimated_improvement + self.estimated_incr

        elif self.mode == 'exponential':
            next_deltas = [delta * self.parameter for delta in deltas]
            next_estimated_improvement = estimated_improvement * self.parameter

        target_value = self.fn_x(next_deltas)

        next_improvement = tf.divide(
            x=(target_value - self.base_value),
            y=tf.maximum(x=next_estimated_improvement, y=util.epsilon)
        )

        return next_x, next_iteration, next_deltas, next_improvement, improvement, next_estimated_improvement