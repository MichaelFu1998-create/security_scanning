def tag(self, label, message=None):
        """Tag the current workdir state."""
        options = ' -m "{}" -a'.format(message) if message else ''
        self.run_elective('git tag{} "{}"'.format(options, label))