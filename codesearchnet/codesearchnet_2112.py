def restore(self, sess, save_path):
        """
        Restores the values of the managed variables from disk location.

        Args:
            sess: The session for which to save the managed variables.
            save_path: The path used to save the data to.
        """

        if self._saver is None:
            raise TensorForceError("register_saver_ops should be called before restore")
        self._saver.restore(sess=sess, save_path=save_path)