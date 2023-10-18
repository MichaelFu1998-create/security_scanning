def process_dir(self, album, force=False):
        """Process a list of images in a directory."""
        for f in album:
            if isfile(f.dst_path) and not force:
                self.logger.info("%s exists - skipping", f.filename)
                self.stats[f.type + '_skipped'] += 1
            else:
                self.stats[f.type] += 1
                yield (f.type, f.path, f.filename, f.src_path, album.dst_path,
                       self.settings)