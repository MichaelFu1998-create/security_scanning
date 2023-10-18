def tf_step(
        self,
        time,
        variables,
        arguments,
        **kwargs
    ):
        """
        Creates the TensorFlow operations for performing an optimization step.

        Args:
            time: Time tensor.
            variables: List of variables to optimize.
            arguments: Dict of arguments for callables, like fn_loss.
            **kwargs: Additional arguments passed on to the internal optimizer.

        Returns:
            List of delta tensors corresponding to the updates for each optimized variable.
        """
        # Get some (batched) argument to determine batch size.
        arguments_iter = iter(arguments.values())
        some_argument = next(arguments_iter)

        try:
            while not isinstance(some_argument, tf.Tensor) or util.rank(some_argument) == 0:
                if isinstance(some_argument, dict):
                    if some_argument:
                        arguments_iter = iter(some_argument.values())
                    some_argument = next(arguments_iter)
                elif isinstance(some_argument, list):
                    if some_argument:
                        arguments_iter = iter(some_argument)
                    some_argument = next(arguments_iter)
                elif some_argument is None or util.rank(some_argument) == 0:
                    # Non-batched argument
                    some_argument = next(arguments_iter)
                else:
                    raise TensorForceError("Invalid argument type.")
        except StopIteration:
            raise TensorForceError("Invalid argument type.")

        batch_size = tf.shape(input=some_argument)[0]
        num_samples = tf.cast(
            x=(self.fraction * tf.cast(x=batch_size, dtype=util.tf_dtype('float'))),
            dtype=util.tf_dtype('int')
        )
        num_samples = tf.maximum(x=num_samples, y=1)
        indices = tf.random_uniform(shape=(num_samples,), maxval=batch_size, dtype=tf.int32)

        subsampled_arguments = util.map_tensors(
            fn=(lambda arg: arg if util.rank(arg) == 0 else tf.gather(params=arg, indices=indices)),
            tensors=arguments
        )

        return self.optimizer.step(
            time=time,
            variables=variables,
            arguments=subsampled_arguments,
            **kwargs
        )