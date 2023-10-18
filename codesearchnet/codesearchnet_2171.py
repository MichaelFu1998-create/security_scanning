def tf_initialize(self):
        """
        Creates tf Variables for the local state/internals/action-buffers and for the local and global counters
        for timestep and episode.
        """

        # Timesteps/Episodes
        # Global: (force on global device; local and global model point to the same (global) data).
        with tf.device(device_name_or_function=(self.global_model.device if self.global_model else self.device)):

            # Global timestep
            collection = self.graph.get_collection(name='global-timestep')
            if len(collection) == 0:
                self.global_timestep = tf.get_variable(
                    name='global-timestep',
                    shape=(),
                    dtype=tf.int64,
                    trainable=False,
                    initializer=tf.constant_initializer(value=0, dtype=tf.int64),
                    collections=['global-timestep', tf.GraphKeys.GLOBAL_STEP]
                )
            else:
                assert len(collection) == 1
                self.global_timestep = collection[0]

            # Global episode
            collection = self.graph.get_collection(name='global-episode')
            if len(collection) == 0:
                self.global_episode = tf.get_variable(
                    name='global-episode',
                    shape=(),
                    dtype=tf.int64,
                    trainable=False,
                    initializer=tf.constant_initializer(value=0, dtype=tf.int64),
                    collections=['global-episode']
                )
            else:
                assert len(collection) == 1
                self.global_episode = collection[0]

        # Local counters: local device
        self.timestep = tf.get_variable(
            name='timestep',
            shape=(),
            dtype=tf.int64,
            initializer=tf.constant_initializer(value=0, dtype=tf.int64),
            trainable=False
        )

        self.episode = tf.get_variable(
            name='episode',
            shape=(),
            dtype=tf.int64,
            initializer=tf.constant_initializer(value=0, dtype=tf.int64),
            trainable=False
        )

        self.episode_index_input = tf.placeholder(
            name='episode_index',
            shape=(),
            dtype=tf.int32,
        )

        # States buffer variable
        for name in sorted(self.states_spec):
            self.list_states_buffer[name] = tf.get_variable(
                name=('state-{}'.format(name)),
                shape=((self.num_parallel, self.batching_capacity,) + tuple(self.states_spec[name]['shape'])),
                dtype=util.tf_dtype(self.states_spec[name]['type']),
                trainable=False
            )

        # Internals buffer variable
        for name in sorted(self.internals_spec):
            self.list_internals_buffer[name] = tf.get_variable(
                name=('internal-{}'.format(name)),
                shape=((self.num_parallel, self.batching_capacity,) + tuple(self.internals_spec[name]['shape'])),
                dtype=util.tf_dtype(self.internals_spec[name]['type']),
                trainable=False
            )

        # Actions buffer variable
        for name in sorted(self.actions_spec):
            self.list_actions_buffer[name]= tf.get_variable(
                name=('action-{}'.format(name)),
                shape=((self.num_parallel, self.batching_capacity,) + tuple(self.actions_spec[name]['shape'])),
                dtype=util.tf_dtype(self.actions_spec[name]['type']),
                trainable=False
            )

        # Buffer index
        # for index in range(self.num_parallel):
        self.list_buffer_index = tf.get_variable(
            name='buffer-index',
            shape=(self.num_parallel,),
            dtype=util.tf_dtype('int'),
            trainable=False
        )