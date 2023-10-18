def _output_file(self, frame):
        """
        If filename was used output a filename, along with multifile
        numbered filenames will be used.

        If buff was specified it is returned.

        :return: Output buff or filename.
        """
        if self.buff:
            return self.buff
        elif self.multifile:
            return self.file_root + "_%03d" % frame + self.file_ext
        else:
            return self.filename