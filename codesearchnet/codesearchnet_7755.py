def big(self):
        """Path to the original image, if ``keep_orig`` is set (relative to the
        album directory). Copy the file if needed.
        """
        if self.settings['keep_orig']:
            s = self.settings
            if s['use_orig']:
                # The image *is* the original, just use it
                return self.filename
            orig_path = join(s['destination'], self.path, s['orig_dir'])
            check_or_create_dir(orig_path)
            big_path = join(orig_path, self.src_filename)
            if not isfile(big_path):
                copy(self.src_path, big_path, symlink=s['orig_link'],
                     rellink=self.settings['rel_link'])
            return join(s['orig_dir'], self.src_filename)