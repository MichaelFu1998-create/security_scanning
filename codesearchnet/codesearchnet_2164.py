def setup_placeholders(self):
        """
        Creates the TensorFlow placeholders, variables, ops and functions for this model.
        NOTE: Does not add the internal state placeholders and initialization values to the model yet as that requires
        the model's Network (if any) to be generated first.
        """

        # States
        for name in sorted(self.states_spec):
            self.states_input[name] = tf.placeholder(
                dtype=util.tf_dtype(self.states_spec[name]['type']),
                shape=(None,) + tuple(self.states_spec[name]['shape']),
                name=('state-' + name)
            )

        # States preprocessing
        if self.states_preprocessing_spec is None:
            for name in sorted(self.states_spec):
                self.states_spec[name]['unprocessed_shape'] = self.states_spec[name]['shape']
        elif not isinstance(self.states_preprocessing_spec, list) and \
                all(name in self.states_spec for name in self.states_preprocessing_spec):
            for name in sorted(self.states_spec):
                if name in self.states_preprocessing_spec:
                    preprocessing = PreprocessorStack.from_spec(
                        spec=self.states_preprocessing_spec[name],
                        kwargs=dict(shape=self.states_spec[name]['shape'])
                    )
                    self.states_spec[name]['unprocessed_shape'] = self.states_spec[name]['shape']
                    self.states_spec[name]['shape'] = preprocessing.processed_shape(shape=self.states_spec[name]['unprocessed_shape'])
                    self.states_preprocessing[name] = preprocessing
                else:
                    self.states_spec[name]['unprocessed_shape'] = self.states_spec[name]['shape']
        # Single preprocessor for all components of our state space
        elif "type" in self.states_preprocessing_spec:
            preprocessing = PreprocessorStack.from_spec(spec=self.states_preprocessing_spec,
                                                        kwargs=dict(shape=self.states_spec[name]['shape']))
            for name in sorted(self.states_spec):
                self.states_spec[name]['unprocessed_shape'] = self.states_spec[name]['shape']
                self.states_spec[name]['shape'] = preprocessing.processed_shape(shape=self.states_spec[name]['unprocessed_shape'])
                self.states_preprocessing[name] = preprocessing
        else:
            for name in sorted(self.states_spec):
                preprocessing = PreprocessorStack.from_spec(
                    spec=self.states_preprocessing_spec,
                    kwargs=dict(shape=self.states_spec[name]['shape'])
                )
                self.states_spec[name]['unprocessed_shape'] = self.states_spec[name]['shape']
                self.states_spec[name]['shape'] = preprocessing.processed_shape(shape=self.states_spec[name]['unprocessed_shape'])
                self.states_preprocessing[name] = preprocessing

        # Actions
        for name in sorted(self.actions_spec):
            self.actions_input[name] = tf.placeholder(
                dtype=util.tf_dtype(self.actions_spec[name]['type']),
                shape=(None,) + tuple(self.actions_spec[name]['shape']),
                name=('action-' + name)
            )

        # Actions exploration
        if self.actions_exploration_spec is None:
            pass
        elif all(name in self.actions_spec for name in self.actions_exploration_spec):
            for name in sorted(self.actions_spec):
                if name in self.actions_exploration:
                    self.actions_exploration[name] = Exploration.from_spec(spec=self.actions_exploration_spec[name])
        else:
            for name in sorted(self.actions_spec):
                self.actions_exploration[name] = Exploration.from_spec(spec=self.actions_exploration_spec)

        # Terminal
        self.terminal_input = tf.placeholder(dtype=util.tf_dtype('bool'), shape=(None,), name='terminal')

        # Reward
        self.reward_input = tf.placeholder(dtype=util.tf_dtype('float'), shape=(None,), name='reward')

        # Reward preprocessing
        if self.reward_preprocessing_spec is not None:
            self.reward_preprocessing = PreprocessorStack.from_spec(
                spec=self.reward_preprocessing_spec,
                # TODO this can eventually have more complex shapes?
                kwargs=dict(shape=())
            )
            if self.reward_preprocessing.processed_shape(shape=()) != ():
                raise TensorForceError("Invalid reward preprocessing!")

        # Deterministic/independent action flag (should probably be the same)
        self.deterministic_input = tf.placeholder(dtype=util.tf_dtype('bool'), shape=(), name='deterministic')
        self.independent_input = tf.placeholder(dtype=util.tf_dtype('bool'), shape=(), name='independent')