def _load_meta(self, size, md5):
        """Set key attributes to retrived metadata. Might be extended in the
        future to support more attributes.
        """
        if not hasattr(self, 'local_hashes'):
            self.local_hashes = {}

        self.size = int(size)

        if (re.match('^[a-fA-F0-9]{32}$', md5)):
            self.md5 = md5