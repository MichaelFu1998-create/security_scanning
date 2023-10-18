def process_file(self):
        """Deprecated."""
        warnings.warn(DeprecationWarning("'self.process_file' is deprecated"))
        return os.path.join(self._raw["config_dir"], self._raw["process"])