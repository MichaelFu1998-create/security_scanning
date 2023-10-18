def _load_credentials(self):
        """(Re-)loads the credentials from the file."""
        if not self._file:
            return

        loaded_credentials = _load_credentials_file(self._file)
        self._credentials.update(loaded_credentials)

        logger.debug('Read credential file')