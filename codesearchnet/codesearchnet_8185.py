def start(self, threaded=None):
        """Creates and starts the project."""
        if threaded is not None:
            self.threaded = threaded
        run = {'run': {'threaded': False}}
        self.project = project.project(
            self.desc, run, root_file=self.project_file)
        self._run = self.project.run
        self._runner.start(self.threaded)