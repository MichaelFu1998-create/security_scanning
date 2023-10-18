def compress(self, filename):
        """Compress a file, only if needed."""
        compressed_filename = self.get_compressed_filename(filename)
        if not compressed_filename:
            return

        self.do_compress(filename, compressed_filename)