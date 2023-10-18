def setup(self):
        """
        Sets up the TensorFlow model graph, starts the servers (distributed mode), creates summarizers
        and savers, initializes (and enters) the TensorFlow session.
        """

        # Create/get our graph, setup local model/global model links, set scope and device.
        graph_default_context = self.setup_graph()

        # Start a tf Server (in case of distributed setup). Only start once.
        if self.execution_type == "distributed" and self.server is None and self.is_local_model:
            self.start_server()

        # build the graph
        with tf.device(device_name_or_function=self.device):
            with tf.variable_scope(name_or_scope=self.scope, reuse=False):

                # Variables and summaries
                self.variables = dict()
                self.all_variables = dict()
                self.registered_variables = set()

                # Build the graph's placeholders, tf_functions, etc
                self.setup_placeholders()
                # Create model's "external" components.
                # Create tensorflow functions from "tf_"-methods.
                self.setup_components_and_tf_funcs()

                # Create core variables (timestep, episode counters, buffers for states/actions/internals).
                self.fn_initialize()

                if self.summarizer_spec is not None:
                    with tf.name_scope(name='summarizer'):
                        self.summarizer = tf.contrib.summary.create_file_writer(
                            logdir=self.summarizer_spec['directory'],
                            max_queue=None,
                            flush_millis=(self.summarizer_spec.get('flush', 10) * 1000),
                            filename_suffix=None,
                            name=None
                        )
                        default_summarizer = self.summarizer.as_default()
                        # Problem: not all parts of the graph are called on every step
                        assert 'steps' not in self.summarizer_spec
                        # if 'steps' in self.summarizer_spec:
                        #     record_summaries = tf.contrib.summary.record_summaries_every_n_global_steps(
                        #         n=self.summarizer_spec['steps'],
                        #         global_step=self.global_timestep
                        #     )
                        # else:
                        record_summaries = tf.contrib.summary.always_record_summaries()

                    default_summarizer.__enter__()
                    record_summaries.__enter__()

                # Input tensors
                states = util.map_tensors(fn=tf.identity, tensors=self.states_input)
                internals = util.map_tensors(fn=tf.identity, tensors=self.internals_input)
                actions = util.map_tensors(fn=tf.identity, tensors=self.actions_input)
                terminal = tf.identity(input=self.terminal_input)
                reward = tf.identity(input=self.reward_input)
                # Probably both deterministic and independent should be the same at some point.
                deterministic = tf.identity(input=self.deterministic_input)
                independent = tf.identity(input=self.independent_input)
                episode_index = tf.identity(input=self.episode_index_input)

                states, actions, reward = self.fn_preprocess(states=states, actions=actions, reward=reward)

                self.create_operations(
                    states=states,
                    internals=internals,
                    actions=actions,
                    terminal=terminal,
                    reward=reward,
                    deterministic=deterministic,
                    independent=independent,
                    index=episode_index
                )

                # Add all summaries specified in summary_labels
                if 'inputs' in self.summary_labels or 'states' in self.summary_labels:
                    for name in sorted(states):
                        tf.contrib.summary.histogram(name=('states-' + name), tensor=states[name])
                if 'inputs' in self.summary_labels or 'actions' in self.summary_labels:
                    for name in sorted(actions):
                        tf.contrib.summary.histogram(name=('actions-' + name), tensor=actions[name])
                if 'inputs' in self.summary_labels or 'reward' in self.summary_labels:
                    tf.contrib.summary.histogram(name='reward', tensor=reward)

                if 'graph' in self.summary_labels:
                    with tf.name_scope(name='summarizer'):
                        graph_def = self.graph.as_graph_def()
                        graph_str = tf.constant(
                            value=graph_def.SerializeToString(),
                            dtype=tf.string,
                            shape=()
                        )
                        self.graph_summary = tf.contrib.summary.graph(
                            param=graph_str,
                            step=self.global_timestep
                        )
                        if 'meta_param_recorder_class' in self.summarizer_spec:
                            self.graph_summary = tf.group(
                                self.graph_summary,
                                *self.summarizer_spec['meta_param_recorder_class'].build_metagraph_list()
                            )

                if self.summarizer_spec is not None:
                    record_summaries.__exit__(None, None, None)
                    default_summarizer.__exit__(None, None, None)

                    with tf.name_scope(name='summarizer'):
                        self.flush_summarizer = tf.contrib.summary.flush()

                        self.summarizer_init_op = tf.contrib.summary.summary_writer_initializer_op()
                        assert len(self.summarizer_init_op) == 1
                        self.summarizer_init_op = self.summarizer_init_op[0]

        # If we are a global model -> return here.
        # Saving, syncing, finalizing graph, session is done by local replica model.
        if self.execution_type == "distributed" and not self.is_local_model:
            return

        # Saver/Summary -> Scaffold.
        self.setup_saver()

        self.setup_scaffold()

        # Create necessary hooks for the upcoming session.
        hooks = self.setup_hooks()

        # We are done constructing: Finalize our graph, create and enter the session.
        self.setup_session(self.server, hooks, graph_default_context)