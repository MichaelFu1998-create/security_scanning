def change(self,
               new_abspath=None,
               new_dirpath=None,
               new_dirname=None,
               new_basename=None,
               new_fname=None,
               new_ext=None):
        """
        Return a new :class:`pathlib_mate.pathlib2.Path` object with updated information.
        """
        if new_abspath is not None:
            p = self.__class__(new_abspath)
            return p

        if (new_dirpath is None) and (new_dirname is not None):
            new_dirpath = os.path.join(self.parent.dirpath, new_dirname)

        elif (new_dirpath is not None) and (new_dirname is None):
            new_dirpath = new_dirpath

        elif (new_dirpath is None) and (new_dirname is None):
            new_dirpath = self.dirpath

        elif (new_dirpath is not None) and (new_dirname is not None):
            raise ValueError("Cannot having both new_dirpath and new_dirname!")

        if new_basename is None:
            if new_fname is None:
                new_fname = self.fname
            if new_ext is None:
                new_ext = self.ext
            new_basename = new_fname + new_ext
        else:
            if new_fname is not None or new_ext is not None:
                raise ValueError("Cannot having both new_basename, "
                                 "new_fname, new_ext!")

        return self.__class__(new_dirpath, new_basename)