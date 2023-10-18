def utime(self, *args, **kwargs):
        """ Set the access and modified times of the file specified by path. """
        os.utime(self.extended_path, *args, **kwargs)