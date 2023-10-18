def tf_initialize(self, x_init, base_value, target_value, estimated_improvement):
        """
        Initialization step preparing the arguments for the first iteration of the loop body.

        Args:
            x_init: Initial solution guess $x_0$.
            base_value: Value $f(x')$ at $x = x'$.
            target_value: Value $f(x_0)$ at $x = x_0$.
            estimated_improvement: Estimated value at $x = x_0$, $f(x')$ if None.

        Returns:
            Initial arguments for tf_step.
        """
        self.base_value = base_value

        if estimated_improvement is None:  # TODO: Is this a good alternative?
            estimated_improvement = tf.abs(x=base_value)

        first_step = super(LineSearch, self).tf_initialize(x_init)

        improvement = tf.divide(
            x=(target_value - self.base_value),
            y=tf.maximum(x=estimated_improvement, y=util.epsilon)
        )

        last_improvement = improvement - 1.0

        if self.mode == 'linear':
            deltas = [-t * self.parameter for t in x_init]
            self.estimated_incr = -estimated_improvement * self.parameter

        elif self.mode == 'exponential':
            deltas = [-t * self.parameter for t in x_init]

        return first_step + (deltas, improvement, last_improvement, estimated_improvement)