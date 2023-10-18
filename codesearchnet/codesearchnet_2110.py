def register_saver_ops(self):
        """
        Registers the saver operations to the graph in context.
        """

        variables = self.get_savable_variables()
        if variables is None or len(variables) == 0:
            self._saver = None
            return

        base_scope = self._get_base_variable_scope()
        variables_map = {strip_name_scope(v.name, base_scope): v for v in variables}

        self._saver = tf.train.Saver(
            var_list=variables_map,
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
        )