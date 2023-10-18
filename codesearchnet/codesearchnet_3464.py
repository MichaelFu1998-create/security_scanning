def _open(self, f):
        """
        Adds a file descriptor to the current file descriptor list

        :rtype: int
        :param f: the file descriptor to add.
        :return: the index of the file descriptor in the file descr. list
        """
        if None in self.files:
            fd = self.files.index(None)
            self.files[fd] = f
        else:
            fd = len(self.files)
            self.files.append(f)
        return fd