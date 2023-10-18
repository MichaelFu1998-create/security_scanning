def _savepath(self, filename):
        """
        Returns the full path for saving the file, adding an extension
        and making the filename unique as necessary.
        """
        (basename, ext) = os.path.splitext(filename)
        basename = basename if (ext in self.extensions) else filename
        ext = ext if (ext in self.extensions) else self.extensions[0]
        savepath = os.path.abspath(os.path.join(self.directory,
                                                 '%s%s' % (basename, ext)))
        return (tempfile.mkstemp(ext, basename + "_", self.directory)[1]
                if self.hash_suffix else savepath)