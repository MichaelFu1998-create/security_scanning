def locked_get(self):
        """Retrieve Credential from file.

        Returns:
            oauth2client.client.Credentials

        Raises:
            IOError if the file is a symbolic link.
        """
        credentials = None
        _helpers.validate_file(self._filename)
        try:
            f = open(self._filename, 'rb')
            content = f.read()
            f.close()
        except IOError:
            return credentials

        try:
            credentials = client.Credentials.new_from_json(content)
            credentials.set_store(self)
        except ValueError:
            pass

        return credentials