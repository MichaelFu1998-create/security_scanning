def setup_scaffold(self):
        """
        Creates the tf.train.Scaffold object and assigns it to self.scaffold.
        Other fields of the Scaffold are generated automatically.
        """
        if self.execution_type == "single":
            global_variables = self.get_variables(include_submodules=True, include_nontrainable=True)
            # global_variables += [self.global_episode, self.global_timestep]
            init_op = tf.variables_initializer(var_list=global_variables)
            if self.summarizer_init_op is not None:
                init_op = tf.group(init_op, self.summarizer_init_op)
            if self.graph_summary is None:
                ready_op = tf.report_uninitialized_variables(var_list=global_variables)
                ready_for_local_init_op = None
                local_init_op = None
            else:
                ready_op = None
                ready_for_local_init_op = tf.report_uninitialized_variables(var_list=global_variables)
                local_init_op = self.graph_summary

        else:
            # Global and local variable initializers.
            global_variables = self.global_model.get_variables(include_submodules=True, include_nontrainable=True)
            # global_variables += [self.global_episode, self.global_timestep]
            local_variables = self.get_variables(include_submodules=True, include_nontrainable=True)
            init_op = tf.variables_initializer(var_list=global_variables)
            if self.summarizer_init_op is not None:
                init_op = tf.group(init_op, self.summarizer_init_op)
            ready_op = tf.report_uninitialized_variables(var_list=(global_variables + local_variables))
            ready_for_local_init_op = tf.report_uninitialized_variables(var_list=global_variables)
            if self.graph_summary is None:
                local_init_op = tf.group(
                    tf.variables_initializer(var_list=local_variables),
                    # Synchronize values of trainable variables.
                    *(tf.assign(ref=local_var, value=global_var) for local_var, global_var in zip(
                        self.get_variables(include_submodules=True),
                        self.global_model.get_variables(include_submodules=True)
                    ))
                )
            else:
                local_init_op = tf.group(
                    tf.variables_initializer(var_list=local_variables),
                    self.graph_summary,
                    # Synchronize values of trainable variables.
                    *(tf.assign(ref=local_var, value=global_var) for local_var, global_var in zip(
                        self.get_variables(include_submodules=True),
                        self.global_model.get_variables(include_submodules=True)
                    ))
                )

        def init_fn(scaffold, session):
            if self.saver_spec is not None and self.saver_spec.get('load', True):
                directory = self.saver_spec['directory']
                file = self.saver_spec.get('file')
                if file is None:
                    file = tf.train.latest_checkpoint(
                        checkpoint_dir=directory,
                        latest_filename=None  # Corresponds to argument of saver.save() in Model.save().
                    )
                elif not os.path.isfile(file):
                    file = os.path.join(directory, file)
                if file is not None:
                    try:
                        scaffold.saver.restore(sess=session, save_path=file)
                        session.run(fetches=self.list_buffer_index_reset_op)
                    except tf.errors.NotFoundError:
                        raise TensorForceError("Error: Existing checkpoint could not be loaded! Set \"load\" to false in saver_spec.")

        # TensorFlow scaffold object
        # TODO explain what it does.
        self.scaffold = tf.train.Scaffold(
            init_op=init_op,
            init_feed_dict=None,
            init_fn=init_fn,
            ready_op=ready_op,
            ready_for_local_init_op=ready_for_local_init_op,
            local_init_op=local_init_op,
            summary_op=None,
            saver=self.saver,
            copy_from_scaffold=None
        )