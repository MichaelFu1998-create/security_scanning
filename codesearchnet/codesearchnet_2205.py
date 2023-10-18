def setup_components_and_tf_funcs(self, custom_getter=None):
        """
        Creates and stores Network and Distribution objects.
        Generates and stores all template functions.
        """
        # Create network before super-call, since non-empty internals_spec attribute (for RNN) is required subsequently.
        self.network = Network.from_spec(
            spec=self.network_spec,
            kwargs=dict(summary_labels=self.summary_labels)
        )

        # Now that we have the network component: We can create the internals placeholders.
        assert len(self.internals_spec) == 0
        self.internals_spec = self.network.internals_spec()
        for name in sorted(self.internals_spec):
            internal = self.internals_spec[name]
            self.internals_input[name] = tf.placeholder(
                dtype=util.tf_dtype(internal['type']),
                shape=(None,) + tuple(internal['shape']),
                name=('internal-' + name)
            )
            if internal['initialization'] == 'zeros':
                self.internals_init[name] = np.zeros(shape=internal['shape'])
            else:
                raise TensorForceError("Invalid internal initialization value.")

        # And only then call super.
        custom_getter = super(DistributionModel, self).setup_components_and_tf_funcs(custom_getter)

        # Distributions
        self.distributions = self.create_distributions()

        # KL divergence function
        self.fn_kl_divergence = tf.make_template(
            name_='kl-divergence',
            func_=self.tf_kl_divergence,
            custom_getter_=custom_getter
        )

        return custom_getter