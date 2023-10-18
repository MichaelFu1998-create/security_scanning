def delete(self):
        """Remove this resource (recursive)."""
        self._check_write_access()
        filepath = self._getFilePath()
        commands.remove(self.provider.ui, self.provider.repo, filepath, force=True)