def load(self, project_file=''):
        """Load/reload the description from a YML file. Prompt if no file given."""
        self._request_project_file(project_file)
        self.clear()
        self.desc.update(data_file.load(self._project_file))