def _create_file_if_needed(self):
        """Create an empty file if necessary.

        This method will not initialize the file. Instead it implements a
        simple version of "touch" to ensure the file has been created.
        """
        if not os.path.exists(self._filename):
            old_umask = os.umask(0o177)
            try:
                open(self._filename, 'a+b').close()
            finally:
                os.umask(old_umask)