def temporary_path(self, extension=""):
        """Saves the dump in a temporary file and returns its path.

        .. warning:: The user of this method is responsible for deleting this
                     file to save space on the hard drive.
                     If you only need a file object for a short period of time
                     you can use the method :meth:`temporary_file`.

        :param str extension: the ending ot the file name e.g. ``".png"``
        :return: a path to the temporary file
        :rtype: str
        """
        path = NamedTemporaryFile(delete=False, suffix=extension).name
        self.path(path)
        return path