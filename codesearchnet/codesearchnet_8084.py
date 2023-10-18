def remove(self):
        """Remove this file from the remote storage."""
        response = self._delete(self._delete_url)
        if response.status_code != 204:
            raise RuntimeError('Could not delete {}.'.format(self.path))