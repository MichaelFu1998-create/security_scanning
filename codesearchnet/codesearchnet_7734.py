def get_compressed_filename(self, filename):
        """If the given filename should be compressed, returns the
        compressed filename.

        A file can be compressed if:

        - It is a whitelisted extension
        - The compressed file does not exist
        - The compressed file exists by is older than the file itself

        Otherwise, it returns False.

        """
        if not os.path.splitext(filename)[1][1:] in self.suffixes_to_compress:
            return False

        file_stats = None
        compressed_stats = None
        compressed_filename = '{}.{}'.format(filename, self.suffix)
        try:
            file_stats = os.stat(filename)
            compressed_stats = os.stat(compressed_filename)
        except OSError:  # FileNotFoundError is for Python3 only
            pass

        if file_stats and compressed_stats:
            return (compressed_filename
                    if file_stats.st_mtime > compressed_stats.st_mtime
                    else False)
        else:
            return compressed_filename