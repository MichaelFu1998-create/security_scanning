def setup_components_and_tf_funcs(self, custom_getter=None):
        """
        Constructs the memory and the optimizer objects.
        Generates and stores all template functions.
        """
        custom_getter = super(MemoryModel, self).setup_components_and_tf_funcs(custom_getter)

        # Memory
        self.memory = Memory.from_spec(
            spec=self.memory_spec,
            kwargs=dict(
                states=self.states_spec,
                internals=self.internals_spec,
                actions=self.actions_spec,
                summary_labels=self.summary_labels
            )
        )

        # Optimizer
        self.optimizer = Optimizer.from_spec(
            spec=self.optimizer_spec,
            kwargs=dict(summary_labels=self.summary_labels)
        )

        # TensorFlow functions
        self.fn_discounted_cumulative_reward = tf.make_template(
            name_='discounted-cumulative-reward',
            func_=self.tf_discounted_cumulative_reward,
            custom_getter_=custom_getter
        )
        self.fn_reference = tf.make_template(
            name_='reference',
            func_=self.tf_reference,
            custom_getter_=custom_getter
        )
        self.fn_loss_per_instance = tf.make_template(
            name_='loss-per-instance',
            func_=self.tf_loss_per_instance,
            custom_getter_=custom_getter
        )
        self.fn_regularization_losses = tf.make_template(
            name_='regularization-losses',
            func_=self.tf_regularization_losses,
            custom_getter_=custom_getter
        )
        self.fn_loss = tf.make_template(
            name_='loss',
            func_=self.tf_loss,
            custom_getter_=custom_getter
        )
        self.fn_optimization = tf.make_template(
            name_='optimization',
            func_=self.tf_optimization,
            custom_getter_=custom_getter
        )
        self.fn_import_experience = tf.make_template(
            name_='import-experience',
            func_=self.tf_import_experience,
            custom_getter_=custom_getter
        )

        return custom_getter