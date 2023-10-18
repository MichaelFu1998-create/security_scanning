def tf_next_step(self, x, iteration, deltas, improvement, last_improvement, estimated_improvement):
        """
        Termination condition: max number of iterations, or no improvement for last step, or  
        improvement less than acceptable ratio, or estimated value not positive.

        Args:
            x: Current solution estimate $x_t$.
            iteration: Current iteration counter $t$.
            deltas: Current difference $x_t - x'$.
            improvement: Current improvement $(f(x_t) - f(x')) / v'$.
            last_improvement: Last improvement $(f(x_{t-1}) - f(x')) / v'$.
            estimated_improvement: Current estimated value $v'$.

        Returns:
            True if another iteration should be performed.
        """
        next_step = super(LineSearch, self).tf_next_step(
            x, iteration, deltas, improvement, last_improvement, estimated_improvement
        )

        def undo_deltas():
            value = self.fn_x([-delta for delta in deltas])
            with tf.control_dependencies(control_inputs=(value,)):
                # Trivial operation to enforce control dependency
                return tf.less(x=value, y=value)  # == False

        improved = tf.cond(
            pred=(improvement > last_improvement),
            true_fn=(lambda: True),
            false_fn=undo_deltas
        )

        next_step = tf.logical_and(x=next_step, y=improved)
        next_step = tf.logical_and(x=next_step, y=(improvement < self.accept_ratio))
        return tf.logical_and(x=next_step, y=(estimated_improvement > util.epsilon))