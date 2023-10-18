def setup_components_and_tf_funcs(self, custom_getter=None):
        """
        Allows child models to create model's component objects, such as optimizer(s), memory(s), etc..
        Creates all tensorflow functions via tf.make_template calls on all the class' "tf_"-methods.

        Args:
            custom_getter: The `custom_getter_` object to use for `tf.make_template` when creating TensorFlow functions.
                If None, use a default custom_getter_.

        Returns: The custom_getter passed in (or a default one if custom_getter was None).
        """

        if custom_getter is None:
            def custom_getter(getter, name, registered=False, **kwargs):
                """
                To be passed to tf.make_template() as 'custom_getter_'.
                """
                if registered:
                    self.registered_variables.add(name)
                elif name in self.registered_variables:
                    registered = True
                # Top-level, hence no 'registered' argument.
                variable = getter(name=name, **kwargs)
                if registered:
                    pass
                elif name in self.all_variables:
                    assert variable is self.all_variables[name]
                    if kwargs.get('trainable', True):
                        assert variable is self.variables[name]
                        if 'variables' in self.summary_labels:
                            tf.contrib.summary.histogram(name=name, tensor=variable)
                else:
                    self.all_variables[name] = variable
                    if kwargs.get('trainable', True):
                        self.variables[name] = variable
                        if 'variables' in self.summary_labels:
                            tf.contrib.summary.histogram(name=name, tensor=variable)
                return variable

        self.fn_initialize = tf.make_template(
            name_='initialize',
            func_=self.tf_initialize,
            custom_getter_=custom_getter
        )
        self.fn_preprocess = tf.make_template(
            name_='preprocess',
            func_=self.tf_preprocess,
            custom_getter_=custom_getter
        )
        self.fn_actions_and_internals = tf.make_template(
            name_='actions-and-internals',
            func_=self.tf_actions_and_internals,
            custom_getter_=custom_getter
        )
        self.fn_observe_timestep = tf.make_template(
            name_='observe-timestep',
            func_=self.tf_observe_timestep,
            custom_getter_=custom_getter
        )
        self.fn_action_exploration = tf.make_template(
            name_='action-exploration',
            func_=self.tf_action_exploration,
            custom_getter_=custom_getter
        )

        return custom_getter