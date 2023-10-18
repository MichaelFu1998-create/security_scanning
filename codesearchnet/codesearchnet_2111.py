def save(self, sess, save_path, timestep=None):
        """
        Saves this component's managed variables.

        Args:
            sess: The session for which to save the managed variables.
            save_path: The path to save data to.
            timestep: Optional, the timestep to append to the file name.

        Returns:
            Checkpoint path where the model was saved.
        """

        if self._saver is None:
            raise TensorForceError("register_saver_ops should be called before save")
        return self._saver.save(
            sess=sess,
            save_path=save_path,
            global_step=timestep,
            write_meta_graph=False,
            write_state=True,  # Do we need this?
        )