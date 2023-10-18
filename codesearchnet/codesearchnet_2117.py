def tf_solve(self, fn_x, x_init, *args):
        """
        Iteratively solves an equation/optimization for $x$ involving an expression $f(x)$.

        Args:
            fn_x: A callable returning an expression $f(x)$ given $x$.
            x_init: Initial solution guess $x_0$.
            *args: Additional solver-specific arguments.

        Returns:
            A solution $x$ to the problem as given by the solver.
        """
        self.fn_x = fn_x

        # Initialization step
        args = self.initialize(x_init, *args)
        # args = util.map_tensors(fn=tf.stop_gradient, tensors=args)

        # Iteration loop with termination condition
        if self.unroll_loop:
            # Unrolled for loop
            for _ in range(self.max_iterations):
                next_step = self.next_step(*args)
                step = (lambda: self.step(*args))
                do_nothing = (lambda: args)
                args = tf.cond(pred=next_step, true_fn=step, false_fn=do_nothing)

        else:
            # TensorFlow while loop
            args = tf.while_loop(cond=self.next_step, body=self.step, loop_vars=args)

        # First argument contains solution
        return args[0]