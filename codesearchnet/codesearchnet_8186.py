def stop(self=None):
        """Stop the builder if it's running."""
        if not self:
            instance = getattr(Runner.instance(), 'builder', None)
            self = instance and instance()
            if not self:
                return

        self._runner.stop()
        if self.project:
            self.project.stop()
            self.project = None