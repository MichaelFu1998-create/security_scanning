def setup_saver(self):
        """
        Creates the tf.train.Saver object and stores it in self.saver.
        """
        if self.execution_type == "single":
            global_variables = self.get_variables(include_submodules=True, include_nontrainable=True)
        else:
            global_variables = self.global_model.get_variables(include_submodules=True, include_nontrainable=True)

        # global_variables += [self.global_episode, self.global_timestep]

        for c in self.get_savable_components():
            c.register_saver_ops()

        # TensorFlow saver object
        # TODO potentially make other options configurable via saver spec.
        self.saver = tf.train.Saver(
            var_list=global_variables,  # should be given?
            reshape=False,
            sharded=False,
            max_to_keep=5,
            keep_checkpoint_every_n_hours=10000.0,
            name=None,
            restore_sequentially=False,
            saver_def=None,
            builder=None,
            defer_build=False,
            allow_empty=True,
            write_version=tf.train.SaverDef.V2,
            pad_step_number=False,
            save_relative_paths=True
            # filename=None
        )