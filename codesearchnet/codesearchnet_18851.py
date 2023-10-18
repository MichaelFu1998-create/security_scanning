def get_filesize(self, filename):
        """ Returns the filesize of a file

        :param filename: the full path to the file on the server.
        :type filename: string

        :returns: string representation of the filesize.
        """
        result = []

        def dir_callback(val):
            result.append(val.split()[4])

        self._ftp.dir(filename, dir_callback)
        return result[0]