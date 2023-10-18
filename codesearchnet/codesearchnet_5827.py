def locked_put(self, credentials):
        """Write Credentials to file.

        Args:
            credentials: Credentials, the credentials to store.

        Raises:
            IOError if the file is a symbolic link.
        """
        self._create_file_if_needed()
        _helpers.validate_file(self._filename)
        f = open(self._filename, 'w')
        f.write(credentials.to_json())
        f.close()