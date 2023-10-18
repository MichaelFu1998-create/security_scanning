def convert(self, value, param, ctx):
        """Return file content if file, else, return value as-is
        """
        # Protect against corner cases of invalid inputs
        if not isinstance(value, str):
            return value
        if isinstance(value, six.binary_type):
            value = value.decode('UTF-8')
        # Read from a file under these cases
        if value.startswith('@'):
            filename = os.path.expanduser(value[1:])
            file_obj = super(Variables, self).convert(filename, param, ctx)
            if hasattr(file_obj, 'read'):
                # Sometimes click.File may return a buffer and not a string
                return file_obj.read()
            return file_obj

        # No file, use given string
        return value