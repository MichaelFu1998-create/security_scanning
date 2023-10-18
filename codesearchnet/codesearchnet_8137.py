def save(self, project_file=''):
        """Save the description as a YML file. Prompt if no file given."""
        self._request_project_file(project_file)
        data_file.dump(self.desc.as_dict(), self.project_file)