def file_supported(cls, filename):
        """
        Returns a boolean indicating whether the filename has an
        appropriate extension for this class.
        """
        if not isinstance(filename, str):
            return False
        (_, ext) = os.path.splitext(filename)
        if ext not in cls.extensions:
            return False
        else:
            return True