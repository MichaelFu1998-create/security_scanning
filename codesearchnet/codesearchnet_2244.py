def setup_components_and_tf_funcs(self, custom_getter=None):
        """
        Constructs the extra Replay memory.
        """
        custom_getter = super(QDemoModel, self).setup_components_and_tf_funcs(custom_getter)

        self.demo_memory = Replay(
            states=self.states_spec,
            internals=self.internals_spec,
            actions=self.actions_spec,
            include_next_states=True,
            capacity=self.demo_memory_capacity,
            scope='demo-replay',
            summary_labels=self.summary_labels
        )

        # Import demonstration optimization.
        self.fn_import_demo_experience = tf.make_template(
            name_='import-demo-experience',
            func_=self.tf_import_demo_experience,
            custom_getter_=custom_getter
        )

        # Demonstration loss.
        self.fn_demo_loss = tf.make_template(
            name_='demo-loss',
            func_=self.tf_demo_loss,
            custom_getter_=custom_getter
        )

        # Combined loss.
        self.fn_combined_loss = tf.make_template(
            name_='combined-loss',
            func_=self.tf_combined_loss,
            custom_getter_=custom_getter
        )

        # Demonstration optimization.
        self.fn_demo_optimization = tf.make_template(
            name_='demo-optimization',
            func_=self.tf_demo_optimization,
            custom_getter_=custom_getter
        )

        return custom_getter