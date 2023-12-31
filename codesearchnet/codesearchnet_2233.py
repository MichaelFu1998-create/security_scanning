def tf_step(
        self,
        time,
        variables,
        arguments,
        fn_loss,
        fn_kl_divergence,
        return_estimated_improvement=False,
        **kwargs
    ):
        """
        Creates the TensorFlow operations for performing an optimization step.

        Args:
            time: Time tensor.
            variables: List of variables to optimize.
            arguments: Dict of arguments for callables, like fn_loss.
            fn_loss: A callable returning the loss of the current model.
            fn_kl_divergence: A callable returning the KL-divergence relative to the current model.
            return_estimated_improvement: Returns the estimated improvement resulting from the  
                natural gradient calculation if true.
            **kwargs: Additional arguments, not used.

        Returns:
            List of delta tensors corresponding to the updates for each optimized variable.
        """

        # Optimize: argmin(w) loss(w + delta) such that kldiv(P(w) || P(w + delta)) = learning_rate
        # For more details, see our blogpost:
        # https://reinforce.io/blog/end-to-end-computation-graphs-for-reinforcement-learning/

        # from tensorforce import util
        # arguments = util.map_tensors(fn=tf.stop_gradient, tensors=arguments)

        # kldiv
        kldiv = fn_kl_divergence(**arguments)

        # grad(kldiv)
        kldiv_gradients = tf.gradients(ys=kldiv, xs=variables)

        # Calculates the product x * F of a given vector x with the fisher matrix F.
        # Incorporating the product prevents having to calculate the entire matrix explicitly.
        def fisher_matrix_product(deltas):
            # Gradient is not propagated through solver.
            deltas = [tf.stop_gradient(input=delta) for delta in deltas]

            # delta' * grad(kldiv)
            delta_kldiv_gradients = tf.add_n(inputs=[
                tf.reduce_sum(input_tensor=(delta * grad)) for delta, grad in zip(deltas, kldiv_gradients)
            ])

            # [delta' * F] = grad(delta' * grad(kldiv))
            return tf.gradients(ys=delta_kldiv_gradients, xs=variables)

        # loss
        loss = fn_loss(**arguments)

        # grad(loss)
        loss_gradients = tf.gradients(ys=loss, xs=variables)

        # Solve the following system for delta' via the conjugate gradient solver.
        # [delta' * F] * delta' = -grad(loss)
        # --> delta'  (= lambda * delta)
        deltas = self.solver.solve(fn_x=fisher_matrix_product, x_init=None, b=[-grad for grad in loss_gradients])

        # delta' * F
        delta_fisher_matrix_product = fisher_matrix_product(deltas=deltas)

        # c' = 0.5 * delta' * F * delta'  (= lambda * c)
        # TODO: Why constant and hence KL-divergence sometimes negative?
        constant = 0.5 * tf.add_n(inputs=[
            tf.reduce_sum(input_tensor=(delta_F * delta))
            for delta_F, delta in zip(delta_fisher_matrix_product, deltas)
        ])

        # Natural gradient step if constant > 0
        def natural_gradient_step():
            # lambda = sqrt(c' / c)
            lagrange_multiplier = tf.sqrt(x=(constant / self.learning_rate))

            # delta = delta' / lambda
            estimated_deltas = [delta / lagrange_multiplier for delta in deltas]

            # improvement = grad(loss) * delta  (= loss_new - loss_old)
            estimated_improvement = tf.add_n(inputs=[
                tf.reduce_sum(input_tensor=(grad * delta))
                for grad, delta in zip(loss_gradients, estimated_deltas)
            ])

            # Apply natural gradient improvement.
            applied = self.apply_step(variables=variables, deltas=estimated_deltas)

            with tf.control_dependencies(control_inputs=(applied,)):
                # Trivial operation to enforce control dependency
                if return_estimated_improvement:
                    return [estimated_delta + 0.0 for estimated_delta in estimated_deltas], estimated_improvement
                else:
                    return [estimated_delta + 0.0 for estimated_delta in estimated_deltas]

        # Zero step if constant <= 0
        def zero_step():
            if return_estimated_improvement:
                return [tf.zeros_like(tensor=delta) for delta in deltas], 0.0
            else:
                return [tf.zeros_like(tensor=delta) for delta in deltas]

        # Natural gradient step only works if constant > 0
        return tf.cond(pred=(constant > 0.0), true_fn=natural_gradient_step, false_fn=zero_step)