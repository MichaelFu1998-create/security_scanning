def _append_log(self, specs):
        """
        The log contains the tids and corresponding specifications
        used during launch with the specifications in JSON format.
        """
        self._spec_log += specs # This should be removed
        log_path = os.path.join(self.root_directory, ("%s.log" % self.batch_name))
        core.Log.write_log(log_path, [spec for (_, spec) in specs], allow_append=True)