def add_file(self, file, **kwargs):
        """Append a file to file repository.

        For file monitoring, monitor instance needs file.
        Please put the name of file to `file` argument.

        :param file: the name of file you want monitor.

        """

        if os.access(file, os.F_OK):

            if file in self.f_repository:
                raise DuplicationError("file already added.")

            self.f_repository.append(file)

        else:
            raise IOError("file not found.")